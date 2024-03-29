import json
import logging
import os

from science_jubilee.labware.Labware import Labware, Well, Location
from science_jubilee.tools.Tool import Tool, ToolStateError, ToolConfigurationError, requires_active_tool

from typing import Tuple, Union


logger = logging.getLogger(__name__)

def tip_check(func):
    """Decorator to check if the pipette has a tip attached before performing an action.
    """
    def wrapper(self, *args, **kwargs):
        if self.has_tip == False:
            raise ToolStateError ("Error: No tip is attached. Cannot complete this action")
        else:
            func(self,*args, **kwargs)
    return wrapper

class Pipette(Tool):
    """ A class representation of an Opentrons OT2 pipette.
    """
    def __init__(self,  index, name, brand, model, max_volume,
                  min_volume, zero_position, blowout_position, 
                  drop_tip_position, mm_to_ul):
        """ Initialize the pipette object

        :param index: The tool index of the pipette on the machine
        :type index: int
        :param name: The name associated with the tool (e.g. 'p300_single')
        :type name: str
        :param brand: The brand of the pipette
        :type brand: str
        :param model: The model of the pipette
        :type model: str
        :param max_volume: The maximum volume of the pipette in uL
        :type max_volume: float
        :param min_volume: The minimum volume of the pipette in uL
        :type min_volume: float
        :param zero_position: The position of the plunger before using a :method:`aspirate` step
        :type zero_position: float
        :param blowout_position: The position of the plunger for running a :method:`blowout` step
        :type blowout_position: float
        :param drop_tip_position: The position of the plunger for running a :method:`drop_tip` step
        :type drop_tip_position: float
        :param mm_to_ul: The conversion factor for converting motor microsteps in mm to uL
        :type mm_to_ul: float
        """        
        super().__init__(index, name, brand = brand, 
                         model = model, max_volume = max_volume, min_volume = min_volume,
                         zero_position = zero_position, blowout_position = blowout_position,
                         drop_tip_position = drop_tip_position, mm_to_ul = mm_to_ul)
        self.has_tip = False
        self.first_available_tip = None
        # self.tool_offset = self._machine.tool_z_offsets[self.index]
        self.is_primed = False 
        self.current_well = None
        

    @classmethod
    def from_config(cls, index, name, config_file: str,
                    path :str = os.path.join(os.path.dirname(__file__), 'configs')):
        
        """Initialize the pipette object from a config file

        :param index: The tool index of the pipette on the machine
        :type index: int
        :param name: The tool name
        :type name: str
        :param config_file: The name of the config file containign the pipette parameters
        :type config_file: str
        :param path: The path to the labware configuration `.json` files for the labware,
                defaults to the 'labware_definition/' in the science_jubilee/labware directory.
        :returns: A :class:`Pipette` object
        :rtype: :class:`Pipette`
        """        
        config = os.path.join(path,config_file)
        with open(config) as f:
            kwargs = json.load(f)

        return cls(index, name, **kwargs)
    
           
    def vol2move(self, vol):
        """Converts desired volume in uL to a movement of the pipette motor axis

        :param vol: The desired amount of liquid expressed in uL
        :type vol: float
        :return: The corresponding motor movement in mm
        :rtype: float
        """        
        dv = vol * self.mm_to_ul # will need to change this value

        return dv
    
    @requires_active_tool
    def prime(self, s=2500):
        """Moves the plunger to the low-point on the pipette motor axis to prepare for further commands
        Note::This position should not engage the pipette tip plunger

        :param s: The speed of the plunger movement in mm/min
        :type s: int
        """
        self._machine.move_to(v=self.zero_position, s = s, wait=True)
        self.is_primed = True

    @requires_active_tool
    def _aspirate(self, vol: float, s:int = 2000):
        """Moves the plunger upwards to aspirate liquid into the pipette tip

        :param vol: The volume of liquid to aspirate in uL
        :type vol: float
        :param s: The speed of the plunger movement in mm/min
        :type s: int
        """
        if self.is_primed == True:
            pass
        else:
            self.prime()

        dv = self.vol2move(vol)*-1
        pos = self._machine.get_position()
        end_pos = float(pos['V']) + dv

        self._machine.move_to(v=end_pos, s=s )
    
    @requires_active_tool
    @tip_check
    def aspirate(self, vol: float, location : Union[Well, Tuple, Location], s:int = 2000):
        """Moves the pipette to the specified location and aspirates the desired volume of liquid

        :param vol: The volume of liquid to aspirate in uL
        :type vol: float
        :param location: The location from where to aspirate the liquid from.
        :type location: Union[Well, Tuple, Location]
        :param s: The speed of the plunger movement in mm/min, defaults to 2000
        :type s: int, optional
        :raises ToolStateError: If the pipette does not have a tip attached
        """
        x, y, z = Labware._getxyz(location)
        
        if type(location) == Well:
            self.current_well = location
        elif type(location) == Location:
            self.current_well = location._labware
        else:
            pass
    
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y)
        self._machine.move_to(z=z)
        self._aspirate(vol, s=s)

    @requires_active_tool
    @tip_check
    def _dispense(self,vol: float, s:int = 2000):
        """Moves the plunger downwards to dispense liquid out of the pipette tip

        :param vol: The volume of liquid to dispense in uL
        :type vol: float
        :param s: The speed of the plunger movement in mm/min
        :type s: int

        Note:: Ideally the user does not call this functions directly, but instead uses the :method:`dispense` method
        """
        dv = self.vol2move(vol)
        pos = self._machine.get_position()
        end_pos = float(pos['V']) + dv
        
        #TODO: Figure out why checks break for transfer, work fine for manually aspirating and dispensing
        #if end_pos > self.zero_position:
        #    raise ToolStateError("Error: Pipette does not have anything to dispense")
        #elif dv > self.zero_position:
        #    raise ToolStateError ("Error : The volume to be dispensed is greater than what was aspirated") 
        self._machine.move_to(v = end_pos, s=s )

    @requires_active_tool
    @tip_check
    def dispense(self, vol: float, location :Union[Well, Tuple, Location], s:int = 2000):
        """Moves the pipette to the specified location and dispenses the desired volume of liquid

        :param vol: The volume of liquid to dispense in uL
        :type vol: float
        :param location: The location to dispense the liquid into. 
        :type location: Union[Well, Tuple, Location]
        :param s: The speed of the plunger movement in mm/min, defaults to 2000
        :type s: int, optional
        :raises ToolStateError: If the pipette does not have a tip attached
        """
        x, y, z = Labware._getxyz(location)
        
        if type(location) == Well:
            self.current_well = location
            if z == location.z:
                z= z+10
            else:
                pass
        elif type(location) == Location:
            self.current_well = location._labware
        else:
            pass
        
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y)
        self._machine.move_to(z=z)
        self._dispense(vol, s=s)

    @requires_active_tool
    @tip_check
    def transfer(self, vol: float, source_well: Union[Well, Tuple, Location],
                 destination_well :Union[Well, Tuple, Location] , s:int = 3000,
                 blowout= None, mix_before: tuple = None,
                 mix_after: tuple = None, new_tip : str = 'always'):
        
        """Transfers the desired volume of liquid from the source well to the destination well

        This is a combination of the :method:`aspirate` and :method:`dispense` steps.
        
        :param vol: The volume of liquid to transfer in uL
        :type vol: float
        :param source_well: The location from where to aspirate the liquid from. 
        :type source_well: Union[Well, Tuple, Location]
        :param destination_well: The location to dispense the liquid into. 
        :type destination_well: Union[Well, Tuple, Location]
        :param s: The speed of the plunger movement in mm/min, defaults to 3000
        :type s: int, optional
        :param blowout: The location to blowout any remainign liquid in the pipette tip
        :type blowout: Union[Well, Tuple, Location], optional
        :param mix_before: The number of times to mix before dispensing and the volume to mix
        :type mix_before: tuple, optional
        :param mix_after: The number of times to mix after dispensing and the volume to mix
        :type mix_after: tuple, optional
        :param new_tip: Whether or not to use a new tip for the transfer. Can be 'always', 'never', or 'once' 

        Note:: :param new_tip: still not implemented at the moment (2023-11-16) 
        """
        #TODO: check that tip picked up and get a new one if not
        
        vol_ = self.vol2move(vol)
        # get locations
        xs, ys, zs = Labware._getxyz(source_well)

        if self.is_primed == True:
            pass
        else:
            self.prime()

        # saves some code if we make a list regardless    
        if type(destination_well) != list:
            destination_well = [destination_well] #make it into a list 

        if isinstance(destination_well, list):
            for well in destination_well:
                xd, yd, zd = Labware._getxyz(well)
            
                self._machine.safe_z_movement()
                self._machine.move_to(x= xs, y=ys)
                self._machine.move_to(z = zs)
                if type(source_well)== Well:
                    self.current_well = source_well
                elif type(source_well)==Location:
                    self.current_well = source_well._labware
                self._aspirate(vol_, s=s)
                
                if mix_before:
                    self.mix(mix_before[0], mix_before[1]) 
                else:
                    pass

                self._machine.safe_z_movement()
                self._machine.move_to(x=xd, y=yd)
                self._machine.move_to(z=zd)
                if type(well)==Well:
                    self.current_well = well
                elif type(well)==Location:
                    self.current_well = well._labware
                self._dispense(vol_, s=s)
                
                if mix_after:
                    self.mix(mix_after[0], mix_after[1]) 
                else:
                    pass

                if blowout is not None:
                    self.blowout()
                else:
                    pass
                # if new_tip == 'always':

                #TODO: need to add new_tip option!
    
    @requires_active_tool
    @tip_check
    def blowout(self,  s : int = 3000):
        """Blows out any remaining liquid in the pipette tip

        :param s: The speed of the plunger movement in mm/min, defaults to 3000
        :type s: int, optional
        """

        well = self.current_well
        self._machine.move_to(z = well.top_ + 5 )
        self._machine.move_to(v = self.blowout_position, s=s)
        self.prime()
    
    @requires_active_tool
    @tip_check
    def air_gap(self, vol):
        """Moves the plunger upwards to aspirate air into the pipette tip

        :param vol: The volume of air to aspirate in uL
        :type vol: float
        """
        #TODO: Add a check to ensure compounded volume does not exceed max volume of pipette
        
        dv = self.vol2move(vol)*-1
        well = self.current_well
        self._machine.move_to(z = well.top_ + 20)
        self._machine.move(v= -1*dv)

    @requires_active_tool
    @tip_check
    def mix(self, vol: float, n: int, s: int = 5000):
        """Mixes liquid by alternating aspirate and dispense steps for the specified number of times

        :param vol: The volume of liquid to mix in uL
        :type vol: float
        :param n: The number of times to mix
        :type n: int
        :param s: The speed of the plunger movement in mm/min, defaults to 5000
        :type s: int, optional
        """
        v = self.vol2move(vol)*-1

        self._machine.move_to(z = self.current_well.top_+2)
        self.prime()
        # self._machine.move(dz = -17)
        
        # TODO: figure out a better way to indicate mixing height position that is not hardcoded
        self._machine.move_to(z= self.current_well.z) 
        for i in range(0,n):
            self._aspirate(vol, s=s)
            #self._machine.move_to(v=v, s=s)
            self.prime(s=s)   

## In progress (2023-10-12) To test
    @requires_active_tool
    @tip_check
    def stir(self, n_times: int = 1, height: float= None):
        """Stirs the liquid in the current well by moving the pipette tip in a circular motion

        :param n_times: The number of times to stir the liquid, defaults to 1
        :type n_times: int, optional
        :param height: The z-coordinate to move the tip to during the stir step, defaults to None
        :type height: float, optional
        :raises ToolStateError: If the pipette does not have a tip attached before stirring or if the pipette is not in a well
        """


        z= self.current_well.z + 0.5  # place pieptte tip close to the bottom
        pos =  self._machine.get_position()
        x_ = float(pos['X']) 
        y_ = float(pos['Y'])
        z_ = float(pos['Z'])  

        # check position first
        if x_ != round(self.current_well.x) and y_ != round(self.current_well.y, 2):
            raise ToolStateError("Error: Pipette shuold be in a well before it can stir")  
        elif z_ != round(z,2):
            self._machine.move_to(z=z)

        radius = self.current_well.diameter/2 -(self.current_well.diameter/6) # adjusted so that it does not hit the walls fo the well 

        for n in range(n_times):
            x_sp = self.current_well.x
            y_sp = self.current_well.y
            I = -1*radius
            J = 0 # keeping same y so relative y difference is 0
            if height:
                Z = z + height
                self._machine.gcode(f'G2 X{x_sp} Y{y_sp} Z{Z} I{I} J{J}')
                self._machine.gcode(f'M400') # wait until movement is completed
                self._machine.move_to(z=z) 
            else:
                self._machine.gcode(f'G2 X{x_sp} Y{y_sp} I{I} J{J}')
                self._machine.gcode(f'M400') # wait until movement is completed

    def update_z_offset(self, tip: bool = None):
        """Shift the z-offset of the tool to account for the tip length

        :param tip: Parameter to indicated whether to add or remove the tip offset, defaults to None
        :type tip: bool, optional
        """
        if isinstance(self.tiprack, list):
            tip_offset = self.tiprack[0].tip_length- self.tiprack[0].tip_overlap
        else:
            tip_offset = self.tiprack.tip_length- self.tiprack.tip_overlap

        if tip == True:
            new_z = self.tool_offset - tip_offset
        else:
            new_z = self.tool_offset

        self._machine.gcode(f'G10 P{self.index} Z{new_z}')

    def add_tiprack(self, tiprack: Union[Labware, list]):
        """Associate a tiprack with the pipette tool

        :param tiprack: The tiprack to associate with the pipette 
        :type tiprack: Union[Labware, list]
        """
        if isinstance(tiprack, list):
            for rack in len(tiprack):
                tips = []
                for t in range(96):
                    tips.append(rack[t])
            
            self.tipiterator = pipette_iterator(tips)
            self.tiprack = tiprack
        else:
            self.tipiterator = pipette_iterator(tiprack)
            self.tiprack = tiprack
        
        self.first_available_tip = self.tipiterator.next()

    @requires_active_tool
    def _pickup_tip(self, z):
        """Moves the Jubilee Z-axis upwards to pick up a pipette tip and stops once the tip sensor is triggered

        :param z: The z-coordinate to move the pipette to
        :type z: float
        :raises ToolStateError: If the pipette already has a tip attached
        """
        if self.has_tip == False:
            self._machine.move_to(z=z, s=800, param = 'H4')
        else:
            raise ToolStateError("Error: Pipette already equipped with a tip.")  
        #TODO: Should this be an error or a warning?     

    @requires_active_tool    
    def pickup_tip(self, tip_ : Union[Well, Tuple] = None):
        """Moves the pipette to the specified location and picks up a tip

        This function can either take a specific tip or if not specified, will pick up the next available 
        tip in the tiprack associated with the pipette.
        
        :param tip_: The location of the pipette tip to pick up, defaults to None
        :type tip_: Union[Well, Tuple], optional
        """
        if tip_ is None:
            tip = self.first_available_tip
        else:
            tip = tip_

        x, y, z = Labware._getxyz(tip)
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y)
        self._pickup_tip(z)
        self.has_tip = True
        self.update_z_offset(tip= True)
        # if tip is not None:
        #     self.first_available_tip =  self.tiprack.next()
        # move the plate down( should be + z) for safe movement
        self._machine.move_to(z= self._machine.deck.safe_z + 10)

        #TODO: This should probably iterate the next available tip so that if you use a tip then replace it, you have to manually specify to go use that tip again rather than it just getting picked up. 

    @requires_active_tool
    def return_tip(self, location: Well = None):
        """Returns the pipette tip to the either the specified location or to where the tip was picked up from

        :param location: The location to return the tip to, defaults to None (i.e. return to where the tip was picked up from)
        :type location: :class:`Well`, optional
        """
        if location is None:
            x, y, z = Labware._getxyz(self.first_available_tip)
        else:
            x, y, z = Labware._getxyz(location)
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y)
        # z moves up/down to make sure tip actually makes it into rack 
        self._machine.move(dz = -25)
        self._drop_tip()
        self._machine.move(dz = 25)
        self.prime()
        self.has_tip = False
        self.update_z_offset(tip=False)

    @requires_active_tool
    def _drop_tip(self):
        """Moves the plunger to eject the pipette tip

        :raises ToolConfigurationError: If the pipette does not have a tip attached
        """
        if self.has_tip == True:
            self._machine.move_to(v= self.drop_tip_position, s= 4000)
        else:
            raise ToolConfigurationError('Error: No pipette tip attached to drop')
        
    def increment_tip(self):
        """Increment the next available tip
        """
        self.first_available_tip = self.tipiterator.next()

    @requires_active_tool
    @tip_check
    def drop_tip(self, location: Union[Well, Tuple]):
        """Moves the pipette to the specified location and drops the pipette tip

        :param location: The location to drop the tip into
        :type location: Union[:class:`Well`, tuple]
        """        
        x, y, z = Labware._getxyz(location)

        self._machine.safe_z_movement()
        if x is not None or y is not None:
            self._machine.move_to(x=x, y=y)
        self._drop_tip()
        self.prime()
        self.has_tip = False
        self.update_z_offset(tip=False)

        self.first_available_tip = self.tipiterator.next()
        # logger.info(f"Dropped tip at {(x,y,z)}")


class pipette_iterator():
    """An iterator for iterating through a tiprack

    :param tiprack: The tiprack to iterate through
    :type tiprack: :class:`Labware`    
    """
    def __init__(self, tiprack):
        """Initialize the tip iterator

        :param tiprack: The tiprack to iterate through
        :type tiprack: :class:`Labware`  
        """

        self.tiprack = tiprack
        self.index = 0

    def next(self):
        """Returns the next available tip in the tiprack

        :raises StopIteration: If there are no more tips available in the tiprack
        :return: The next available tip in the tiprack
        :rtype: :class:`Well`
        """
        # print('Pipette tips iterated')
        try:
            result = self.tiprack[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration
        return result

    def prev(self):
        """Returns the previous available tip in the tiprack

        :raises StopIteration: If the current pipette tip is the first tip in the tiprack
        :return: _description_
        :rtype: _type_
        """

        self.index -= 1
        if self.index < 0:
            raise StopIteration
        return self.tiprack[self.index]

    def __iter__(self):
        return self
