.. _modifying_docs:

******************
Modifying the docs
******************

To build the documentation, ensure the virtual environment is activated. Then, ::

    cd docs
    make html

If you are adding new documentation pages, make sure to add a label at the top of your new `.rst` file like so::

    .. _<label>:

where you should replace `<label>` (including the <>) with your label name. You can preview the changes in the `build/html` folder; the build folder is added to the `.gitignore` by default and so won't be pushed to the repo.
    