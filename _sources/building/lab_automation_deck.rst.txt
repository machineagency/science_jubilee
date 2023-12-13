.. _lab_automation_deck:

*******************
Lab Automation Deck
*******************

.. figure:: _static/deck.png
    :scale: 50 %
    :alt: deck
    
    A lab automation deck with a variety of labware installed.

Last Edited: Blair, 2023.11.30

There is also a lab automation deck documented `on the Jubilee Wiki <https://jubilee3d.com/index.php?title=Lab_Automation_Plate>`_. The deck attachment here is easier to build, requires less materials, and has slots off the build plate for disposal (e.g. sharps) containers. It also uses a flexure based design to accommodate slight labware heterogeneity. If you are working with more dangerous or expensive materials, the attachment on the Jubilee Wiki can provide greater stability. 

Parts to Buy
============
*  `1/8" Delrin <https://www.onlinemetals.com/en/buy/plastic/0-125-acetal-sheet-homopolymer-delrin-natural/pid/6761>`_

Parts to Fabricate
==================
* Design files for the deck can be found `here <https://github.com/machineagency/science_jubilee/tree/main/tool_library/bed_plate/fabrication_files>`_

Duet Config Files
=================
* The Jubilee homing routine needs to be adjusted to probe points on the platform, rather than the deck attachment. Find the udpated config files here `here <https://github.com/machineagency/science_jubilee/tree/main/tool_library/bed_plate/duet_config>`_
