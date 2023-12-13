.. _installation:

************
Installation
************

Last Edited: Blair, 2023.11.11

To install ``science_jubilee``:

* Clone the repositository: ``git clone https://github.com/machineagency/science_jubilee.git``
* We recommend using virtual environments to handle dependencies-- see `here <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment>`_ for more information on virtual environments. To do this:

  * Move into the new directory: ``cd science_jubilee``
  * Create a virtual environment named ``.venv``: ``python3 -m venv .venv``
  * Activate the virtual environment: ``source .venv/bin/activate`` 
  * You should now see ``(.venv)`` to the left of your command line prompt! (If you wish to leave the virtual environment, type ``deactivate`` from any directory)
*  Make sure you're using the latest version of pip: ``python3 -m pip install --upgrade pip``
* Install the science_jubilee package: ``python3 -m pip install -e .``
* Installation complete! Whenever you try to run programs using ``science_jubilee``, be sure to activate the virtual environment that you created.

Jupyter Notebooks
=================
To use ``science_jubilee`` from within Jupyter notebooks:

* If you do not already have JupyterLab installed, do so from outside of your virtual environment: ``python3 -m pip install jupyterlab``. You can install 
* Activate the virtual environment where ``science_jubilee`` is installed
* Add your virtual environment to Jupyter: ``python3 -m ipykernel install --user --name=<your_kernel_name>``
* Launch JupyterLab: `jupyter lab`
* When creating notebooks, be sure to choose the kernel you just added!
