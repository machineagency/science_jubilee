.. _contributing_code:

****************************
Code Contribution Guidelines
****************************

Issues
======

Most development starts with a GitHub Issue-- see more about issues `here <https://machineagency.github.io/science_jubilee/development/index.html>`_.

Working on the ``science_jubilee`` Codebase
===========================================

Once an issue has been discussed and assigned to you, you can begin implementing your changes! This involves 'forking' the repository (i.e. copying the repository to your personal GitHub account), making your changes, and then submitting a 'Pull Request' to add your functionality to the main repository. There are a certain set of steps to follow to make sure this goes smoothly. We'll go into more detail on each of them here!


Forking the Codebase
--------------------

The first step to work on the codebase is to fork the repository.  A 'fork' will copy the repository to your personal GitHub account so you can make and test your changes without affecting the base ``science_jubilee`` repo. Then, we can set up our workspace to make changes.

1. **Fork the repository.** From the main ``science_jubilee``, you'll see a 'Fork' button just above the 'About' section. Click on this button and follow any pop-ups that appear.
2. **Clone your fork.** Once you create a fork, you can go to your fork's page on your own GitHub account. You can then clone (or download a copy) of your fork. To do so, click the green 'Code' button and copy the URL. Then, run the following command from the folder where you want to keep your repository::

    git clone <url>

Where you should replace ``<url>`` with the url you just copied. After running this command, you should see all of the ``science_jubilee`` files on your computer.

3. **Add the upstrem repository.** In git, 'upstream' refers to the original repository. To make sure we can sync up with the base repository, we have to explictly set ``science_jubilee`` as the upstream repository. To do this, run the following command from the folder where you cloned the repository::

    git remote add upstream https://github.com/machineagency/science_jubilee.git

For more details on configuring a remote repositorry for a fork, you can take a look at the `GitHub Documentation page <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-repository-for-a-fork>`_.

4. **Make a new branch with a descriptive name.** It's useful to name your branch something descriptive, so that it is quickly clear what changes are being made. To do so, run the following command from the folder where you cloned the repository::

    git checkout -b <descriptive_branch_name>

Where you should replace ``<descriptive_branch_name>`` with your new name. For example, if I were adding a new camera tool, I might name my branch ``new-camera-tool``.

5. **Install the requirements.** You can now install the requirements to use ``science_jubilee``. Take a look at the `Installation <https://machineagency.github.io/sceience_jubilee/getting_started/installation.html#installation>`_ page for a reminder on how to do this.

You should now be set up to make you changes!

Git Workflow
------------

*TODO: Add info on unit tests, once those are implemented*
As you make your changes, be sure to test often. This is to ensure that other code doesn't break when making your changes. Once unit tests are implemented, we'll add more details here.

As you're working on the codebase, you'll need to commit your changes to git. A 'commit' records the changes to a set of files. It can get confusing if you make too many changes in a single commit (e.g. it's hard to figure out where things are going wrong if something isn't working), or if you commit too many small changes (e.g. no need to make a commit after a change to a single line of code if you're going to make other related changes). A good rule of thumb is to commit whenever you've finished a task that can be summarized in a sentence-- use you best judgement!

A standard git workflow for commiting changes is:
1. **Check your changes.** Run ``git status`` to see a list of your modified, added, and deleted files. Look through this list and make sure that it looks right. If there are files there that you didn't expect, you can double-check the changes by running ``git diff``. If there are changes there that you did not intend, you should restore them back to their original state.  You should not commit changes to any files which are not relevant to your specific pull request.
2. **Choose the files to add to your commit.** To add all of the files listed from step 1, you can run ``git add .``, where the period ``.`` means 'everything'.
3. **Commit your changes.** Run ``git commit -m <commit_message>`` to commit the changes. You should replace ``<commit_message>`` with a short description of the changes. Avoid generic statements; for example, instead of something like ``Fixed Machine.py``, say ``Fixed hardcoded values in gcode() method``.
4. Repeat as needed after you make more changes!


Creating a Pull Request
-----------------------

With your changes made and tested, you can submit a pull request (PR). A pull request is a method by which changes from one repository (e.g. your fork) can be merged into another (e.g. the base ``science_jubilee`` repo). To submit a pull request:

1. **Push your changes.** With all changes comitted, run the command::
    
    git push -u origin <branch_name>
    
Where you should replace ``<branch_name>`` with the name of you current branch. When you navigate to your fork page on GitHub, you should now see your changes.

2. **Create the pull request.** On your fork page on GitHub, click the 'Contribute' button just above the list of files. You should have an option to 'Open pull request'. There is a template to fill out. In particular, you should: title the pull request something descriptive, add the issue numbers which are being resolved or addressed, and give a description of what you changed. The goal here is to give enough detail that someone else can take a look at your code to approve it. After adding this info, you can 'Create pull request'.

3. **Resolve any conflicts.** Near the bottom of your pull request, you should see that "This branch has no conflicts with the base branch". A 'conflict' is when the remote version of a file has also been updated since you made your changes, and git doesn't know how to automatically resolve these difference. If you see that "This branch has conflicts that must be resolved", then we need to manually choose what code to keep. If you are unsure of how to resolve the conflicts, leave a comment on the PR and someone else can try to help!

If all is well, then your PR should be merged as soon as a project maintainer has time to look at it!


*Acknowledgements: The info and structure of this page is adapted from the* `p5.js project contribution documentation <https://p5js.org/contributor-docs/#/contributor_guidelines>`_!*