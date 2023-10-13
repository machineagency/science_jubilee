import json
import logging
import os
import sys
import signal
import time
import digitalio
import board
import busio
import adafruit_mcp4725



from labware.Labware import  Well, Location
from .Tool import Tool, ToolStateError, ToolConfigurationError
from typing import Tuple, Union


logger = logging.getLogger(__name__)



class Sonicator(Tool):

    def __init__(self, machine, index, name):
        #TODO:Removed machine from init, check if this should be asigned here or is added later
        super().__init__(index, name)
        self._machine = machine
        self.is_active_tool = False # TODO: add a way to change this to True/False and check before performing action with tool
        self.tool_offset = self._machine.tool_z_offsets[self.index]
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.dac = adafruit_mcp4725.MCP4725(self.i2c, address=0x60)
        self.sonicator_enable = digitalio.DigitalInOut(board.D4)
        self.sonicator_enable.direction = digitalio.Direction.OUTPUT
        self.sonicator_enable.value = False
        self.dac.normalized_value = 0.0


    @staticmethod
    def _getxyz(location: Union[Well, Tuple, Location]):
        if type(location) == Well:
            x, y, z = location.x, location.y, location.z
        elif type(location) == Tuple:
            x, y, z = location
        elif type(location)==Location:
            x,y,z= location[0]
        else:
            raise ValueError("Location should be of type Well or Tuple")
        
        return x,y,z


    def _sonicate(self, exposure_time: float = 1.0, power: float = 0.4,
                 pulse_duty_cycle: float = 0.5, pulse_interval: float = 1.0, verbose:bool = False):
        """enable the sonicator at the power level for the exposure time."""
        # Quick sanity checks
        assert 0 <= power <= 1.0, \
            f"Error: power must be between 0.0 and 1.0. Value specified is: {power}"
        assert 0 <= pulse_duty_cycle <= 1.0, \
            f"Error: pulse_duty_cycle must be between 0.0 and 1.0. Value specified is: {pulse_duty_cycle}"
        assert pulse_interval > 0, \
            f"Error: pulse_interval must be positive. Value specified is: {pulse_interval}."
        assert pulse_interval <= exposure_time, \
            f"Error: pulse_interval cannot exceed exposure time. Value specified is: {pulse_interval}, " \
            f"but total exposure time is {exposure_time}."

        self.dac.normalized_value = power
        on_interval = pulse_duty_cycle * pulse_interval
        off_interval = (1 - pulse_duty_cycle) * pulse_interval

        start_time = time.perf_counter()
        stop_time = exposure_time + start_time
        while True:
            # On interval.
            curr_time = time.perf_counter()
            if curr_time + on_interval < stop_time:
                if verbose:
                    print(f"{time.perf_counter() - start_time :.2f} | Sonicator on.")
                else:
                    pass
                self.sonicator_enable.value = True
                time.sleep(on_interval)
            elif stop_time > curr_time: # last time to sleep.
                if verbose:
                    print(f"{time.perf_counter() - start_time :.2f} | Sonicator on.")
                else:
                    pass
                self.sonicator_enable.value = True
                time.sleep(stop_time - curr_time)

            # Off interval.
            curr_time = time.perf_counter()
            if curr_time + off_interval < stop_time:
                if verbose:
                    print(f"{time.perf_counter() - start_time :.2f} | Sonicator off.")
                else:
                    pass
                self.sonicator_enable.value = False
                time.sleep(off_interval)
            elif stop_time > curr_time: # last time to sleep.
                if verbose:
                    print(f"{time.perf_counter() - start_time :.2f} | Sonicator off.")
                else:
                    pass
                self.sonicator_enable.value = False
                time.sleep(stop_time - curr_time)
                break
            else:
                if verbose:
                    print(f"{time.perf_counter() - start_time :.2f} | Sonicator off.")
                else:
                    pass
                break
        
        print(f"{time.perf_counter() - start_time :.2f} | Finished sonicating.")
        self.sonicator_enable.value = False
        self.dac.normalized_value = 0

    def sonicate_well(self, location:Union[Well, Tuple, Location],
                        plunge_depth: float, sonication_time: float,
                        power: float, pulse_duty_cycle: float, pulse_interval: float,
                        autoclean: bool = True, verbose:bool = False, *args):
        """Sonicate one well at a specified depth for a given time. Then clean the tip.
            deck_index: deck index where the plate lives
            row_letter: row coordinate to sonicate at
            column_index: number coordinate to sonicate at
            plunge_depth: depth (in mm) to plunge from the top of the plate.
            seconds: time (in sec) to sonicate for
            power: sonicator power level ranging from 0.4 (default, min) through 1.0 (max).
            autoclean: whether or not to perform the predefined autoclean routine.

            Note: sonicator does not turn on below power level of 0.4.
        """

        #Check that plunger depth is compatible with labware dimensions
        if type(location) == Well:
            plate_height = location.top_
        elif type(location)==Location:
            plate_height= location[1].top_
        elif type(location) == Tuple:
            try:
                plate_height = args['depth']
            except ValueError:
                print('If location is of type {}, parameter "depth" needs to be indicated'.format(type(location)))        


        plunge_height = plate_height - plunge_depth
        # Sanity check that we're not plunging too deep. Plunge depth is relative.
        
        if plunge_height < 0:
            raise ValueError("Error: plunge depth is too deep.")

        if self._machine.active_tool_index != self.index:
            raise ToolStateError('The {} is not the current active tool. Park the tool in use and pick up the {} with tool index {}'.format(self.name, self.name, self.index))

        x, y, z  = self._getxyz(location)

        self._machine.safe_z_movement()
        self._machine.move_to(x=x,y=y) # Position over the well at safe z height.
        self._machine.move_to(z=plunge_height, wait=True)
        print(f"Sonicating for {sonication_time} seconds!!")
        self._sonicate(sonication_time, power, pulse_duty_cycle, pulse_interval, verbose=verbose)
        print("done!")
        self._machine.safe_z_movement()
   
   
   # TODO: Implement autocleaning
        # if autoclean:
            # self.cleanining_protocol()
 
    # def cleanining_protocol(self, protocol_config: str, paht:str = None):



    def __exit__(self, *args):
        """Cleanup."""
        self.sonicator_enable.value = False
        self.dac.normalized_value = 0