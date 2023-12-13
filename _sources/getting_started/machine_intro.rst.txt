.. _machine_guide:

***************************
Intro to the Machine Driver
***************************

Last Edited: Blair, 2023.11.13

This guide walks you through the basics of using ``science_jubilee`` to control your machine. It assumes you have an understanding of key concepts, and that you have a working motion platform with tools configured.

Connecting to the Machine
=========================

The ``Machine.py`` module is responsible for moving the machine around. To use it in code, we need to import it:: 

  from science_jubilee.Machine import Machine

Then, we can instantiate a new machine and move around!:: 

  m = Machine()                 # a new machine, called 'm'
  m.move_to(x=100, y=50, z=200) # moves to the absolute position (100, 50, 200)
  m.move_to(x=75)               # moves to the absolute position (75, 50, 200)
  m.move(dz=-50)                # moves -50 in the z direction to (75, 50, 150)

Note that absolute moves (``m.move_to``) use the parameters ``x``, ``y``, and ``z``, while relative moves ``m.move`` expect ``dx``, ``dy``, and ``dz``. This is to ensure we don't accidentally move using relative positions when we meant to use absolute (or vice versa). The machine object has numerous useful properties that you might want to access, such as the currently selected tool, current position, or tools which have been configured:: 

  print(m.tool)  # prints the active tool
  print(m.tools) # prints all available tools

See the reference for all available properties. 

Using Tools
===========

To use a tool, we need to import the associated Python module at the top of our file. If we have a camera tool, for example, our import statements would read:: 

  from science_jubilee.Machine import Machine
  from science_jubilee.Camera import Camera

Each tool module follows the same syntax: ``from science_jubilee.N import N``, where ``N`` is the type of tool. We then need to instantiate a new tool with a number & name, and load it on the machine::

  camera = Camera(1, "my_camera") # a new camera, with ID 1 and name "my_camera"
  m.load(camera)

We instantiate the tool with ``(<tool_id>, <name>)``, where ``tool_id`` should match the Duet configuration for the tool on the machine. The ``name`` can be any string that you'd like to refer to this tool as. Both should be unique in your program. We can then pickup this tool by any of its identifiers::

  m.pickup_tool(camera)      # picks up the camera tool
  m.pickup_tool(1)           # picks up tool 1
  m.pickup_tool("my_camera") # picks up tool with name "my_camera"

Now we can build up more complex movements! For example, to take pictures every 10mm between x=100mm and x=200mm::

  # import the relevant modules
  from science_jubilee.Machine import Machine
  from science_jubilee.Camera import Camera

  # load the camera
  camera = Camera(1, "my_camera") # a new camera, with ID 1 and name "my_camera"
  m.load(camera)

  # pickup the camera and move to the start position
  m.pickup(camera)
  m.move_to(x=100, y=0, z=50)

  for x_position in range(100, 200, 10):
    m.move(x=x_position)
    # do something with the camera

For more details on the functionality of each tool, see the reference.

  


