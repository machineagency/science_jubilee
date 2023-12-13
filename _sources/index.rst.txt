.. science_jubilee documentation master file, created by
   sphinx-quickstart on Mon Oct  2 14:56:41 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

🔬🧪 Science Jubilee ⚡⚙️
========================
Welcome to the Science Jubilee docs! This website contains information for lab automation using `Jubilee <https://jubilee3d.com/index.php?title=Main_Page>`_. To get started, check out our guides:

.. grid:: 1 2 2 2
    :gutter: 4
    :padding: 2 2 0 0
    :class-container: sd-text-center

    .. grid-item-card:: Getting Started
        :class-card: intro-card
        :shadow: md

        The getting started guides help you start using ``science_jubilee`` to control your machine, including installation, examples, and introduction to key concepts.

        +++

        .. button-ref:: getting_started
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            Getting Started Guides

    .. grid-item-card:: Building a Science Jubilee
        :class-card: intro-card
        :shadow: md

        The build guides contain information to build existing tools for use on your Science Jubilee, as well as resources to assemble the Jubilee motion platform itself.

        +++

        .. button-ref:: building
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            Build Guides

    .. grid-item-card::  API Reference
        :class-card: intro-card
        :shadow: md

        The reference contains a detailed description of
        the API. It assumes that you have an understanding of the key concepts.

        +++

        .. button-link:: https://machineagency.github.io/science_jubilee/autoapi/index.html
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            Reference

    .. grid-item-card::  Community Contributions
        :class-card: intro-card
        :shadow: md

        Want to add a new tool design or feature? The contributing guides provide information on how you can help improve and expand ``science_jubilee``.

        +++

        .. button-ref:: development
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            Contributing Guides

What is a Science Jubilee?
--------------------------

`Jubilee <https://jubilee3d.com/index.php?title=Main_Page>`_ is an open-source & extensible multi-tool motion platform. If that doesn't mean much to you, you can think of it as a 3D printer that can change its tools. ``science_jubilee`` provides tools and associated control software to use Jubilee for laboratory automation. This website contains documentation for various lab automation applications including liquid handling, imaging, and sample manipulation. While these applications might cater exactly to your planned use case, they most likely will not! ``science_jubilee`` is meant to be flexible; hopefully, the examples here provide a foundation for you to design all sorts of niche experiments.

|pipetting| |duckweed|

.. |pipetting| image:: _static/pipetting.gif
   :width: 49%

.. |duckweed| image:: _static/lm-loop.gif
   :width: 49%


Jubilee is used in various scientific contexts. A few examples include:

* `The Duckbot <https://github.com/machineagency/duckbot>`_, for automating duckweed experiments
* `Sonication Station <https://github.com/machineagency/sonication_station/>`_, for sonicating samples
* `Jubiris <https://github.com/bunnie/jubiris/tree/main>`_, for Infra-Red, In-Situ (IRIS) inspection of silicon

We hope that ``science_jubilee`` helps you add to this list-- if you're using Jubilee for lab automation, reach out to be added here!



Join the Community!
-------------------
* Whether you've built a Jubilee or are just interested in what sorts of things other people are up to, we encourage you to `join the Jubilee Builders & Extenders Discord <https://discord.gg/jubilee>`_! There's a large community of Jubilee builders doing all sorts of things there; you might be particularly interested in the `#lab-automation` channel.
* For a more focused discussion, you can also join our `Open Source Lab Automation Discord <https://discord.com/invite/j9Bqv3djvN>`_!

.. toctree::
   :maxdepth: 5
   :hidden:

   getting_started/index
   building/index
   development/index