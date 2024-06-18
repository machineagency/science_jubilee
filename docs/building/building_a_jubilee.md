---
title: Science Jubilee Build Instructions
---

(jubilee-build-resources)=
# Science Jubilee Build Instructions

So, you're ready to build a Science Jubilee! This guide is a complete set of instructions to get you set up and running, from hardware and tools to building and software setup.

To supplement the text, we also have an ongoing series of build along videos. Check out the intro here:

```{youtube} 8JUbr9aU8eQ
```

## Hardware

The parts to build a Jubilee have been consolidated into [a kit by Filastruder](https://www.filastruder.com/collections/jubilee/products/jubilee-motion-platform-kit). No royalties are provided to Machine Agency for these sales, but Filastruder works with Machine Agency to ensure the parts are of suitable quality and tolerance.

We recommend the following kit options for a Science Jubilee build:

| Option Category | Selection |
| --- | --- |
Extrusion Anodization Color| `Purple` or `Blue` |
| Printed Parts Color[^prints] | `Orange`, `Blue`, or `Black` |
| Panel Options | `Back and side panels (white)` |
| Bed Plate Options | `PEI Plate and Magnetic Sticky Sheet` |
| Bed Heater Options[^heater] | `None` |
| Electronics[^duet] | `Duet 3 Mini Ethernet + 3HC (up to 2 tools)` |
| Electronics Expansion | `+1 3HC Expansion (up to 5 tools total)` |

**NOTE: You will also need to purchase [a Raspberry Pi 5 kit](https://www.raspberrypi.com/products/raspberry-pi-5/?variant=raspberry-pi-5-desktop-kit-us) separately**[^duet].

Check out the Sourcing video to to see how to order the kit:

```{youtube} or2Qg8UBInM
```

[^prints]: Luke's Laboratory also sells [a set of Jubilee 3D printed parts](https://lukeslabonline.com/products/jubilee-printed-parts-kit-asa?variant=40134863651001) in case the 3D printed parts are out of stock on Filastruder. This is the recommended option for Science Jubilee, and the build instructions here are based on the specific configuration in the kit. No royalties are given to us; however, Filastruder and Lukes Laboratory work with us to ensure the parts are of suitable quality and tolerance to meet the needs of a Jubilee build.
[^heater]: `None` assumes you don't plan to use it as an FDM 3D printer or perform experiments with the entire bed heated; otherwise, you can choose `120v, 750W Keenovo Heater w/ 150C Thermal Cutoff & SSR` (assumes North America).
[^duet]: Both the Ethernet and WiFi version can be controlled via a Raspberry Pi (e.g., RPi 4B, RPi 5) by directly connecting to the Duet 3 Mini, which we recommend. This allows you to connect to a variety of WiFi networks (e.g., WPA2-Personal, WPA2-Enterprise), which means connecting to networks such as Eduroam is supported. By contrast, the `Duet 3 Mini WiFi + 3HC` (without a Raspberry Pi connected) can only connect to 2.4 GHz WPA2-personal networks, which means 5G networks and networks like Eduroam typical of academic, government, and industry settings are not supported. While both the Ethernet and WiFi `Duet 3 Mini + 3HC` versions can be used with a Raspberry Pi, we recommend the Ethernet version primarily because it can simplify troubleshooting if you have any issues with the Raspberry Pi Duet 3 Mini firmware. Aside: For laboratory automation in general, you may consider [implementing a standalone IoT network](https://github.com/sparks-baird/self-driving-lab-demo/discussions/83) to support microcontrollers such as the Raspberry Pi Pico W, which can be used within custom Jubilee tools.

## Tools

You will need to procure some tools on your own, but some are already available in the Filastruder kit.

### To buy
- Calipers [[US Amazon](https://www.amazon.com/Neiko-01407A-Electronic-Digital-Stainless/dp/B000GSLKIW)]
- Wire Cutters [[US Amazon](https://www.amazon.com/Hakko-CHP-170-Micro-Cutter/dp/B076M3ZHBV)]
- SN-2549 Wire Crimpers [[US Amazon](https://www.amazon.com/gp/product/B01N4L8QMW)]
- Arbor Press [[US Amazon](https://www.amazon.com/Palmgren-AP05-0-5-Arbor-Press/dp/B01MQD4CNR)]
- Soldering iron [[US Amazon](https://www.amazon.com/Weller-SP40NUS-40-Watt-Soldering-Iron/dp/B00B3SG6UQ?th=1)] (*treat this one as dedicated tool meant only for heat set inserts*)
- Thin flathead screwdriver (*for replacing the default soldering tip with the heatset insert tip*) and Phillips-head screwdriver (*for (un)screwing terminal plugs on the power supply*) [[US Amazon, 6-piece set](https://www.amazon.com/Magnetic-Screwdriver-Professional-Screwdrivers-Improvement/dp/B08XY5C41N/) (untested)]
- 4" reusable cable ties [[US Amazon](https://www.amazon.com/Adjustable-Organizer-Multi-purpose-Management-Organizing/dp/B0CJ52WJZY/?th=1)]
- 8" reusable cable ties [[US Amazon](https://www.amazon.com/Adjustable-Organizer-Multi-purpose-Management-Organizing/dp/B0CJ4W5VN5/?th=1)]

### Already included in kit
Certain tools are already included in the Filastruder kit. This information is included for your reference.
- Hex key 1.5 mm (not ball end) (alternative: [[1.5 mm ball end hex key, US McMaster-Carr](https://www.mcmaster.com/5497a51)])
- Ball end hex keys (2.0 mm, 2.5 mm, 3.0 mm) (alternatives: [[2.0 mm, US McMaster-Carr](https://www.mcmaster.com/5497a52)], [[2.5 mm, US McMaster-Carr](https://www.mcmaster.com/5497a53)], [[3.0 mm, US McMaster-Carr](https://www.mcmaster.com/5497a54)], NOTE: the ones from the kit do not include a grip handle)
- 2-pack of 4-inch Quick-Grip Clamps (NOTE: you will need to remove the pin on the end of the bar; alternative [US Amazon](https://www.amazon.com/IRWINQUICK-GRIPOne-Handed-Micro-Clamp-Pack-1964747/dp/B00004SBCO) (no modification required))
- Threadlocker Blue (2.5 mL) (alternative: [Vibra-Tite](https://www.amazon.com/Permatex-24200-Medium-Strength-Threadlocker/dp/B0002UEMZ2))
- M3-M4 Heatset Insert Installation Tip (alternative: [[US McMaster-Carr](https://www.mcmaster.com/92160a115)])
- Set of 2 25-50-75mm machinist blocks (alternative: [[US Amazon](https://www.amazon.com/BL-25-50-75-Pair-Precision-Steel-Blocks/dp/B002HIYZJU)])
- M3 Hex Nut Driver (alternatives: [[Filastruder](https://www.filastruder.com/products/5-5mm-nut-driver?variant=17989593104455)], [[US Amazon](https://www.amazon.com/gp/product/B00G2DNXV2/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)])
- 100-pack of 2.5mm (0.1in.) thick zip ties

### Additional Notes

You will also need a flat surface during assembly, ideally one that is somewhat heat tolerant when dealing with heatset inserts. Wear protective eyewear (e.g., [[US Amazon](https://www.amazon.com/BK310AF-Polycarbonate-Anti-Fog-Safety-Non-Slip/dp/B009A658JS/)]) while working with hand tools, especially while using a soldering iron, cutting springs, and press-fitting components.

(assembly-instructions)=
## Assembly Instructions

The instructions must be completed sequentially from Section 1 to Section 3. Instructions in the same section don’t explicitly depend on each other, so they can be done at the same time with a friend. In total, plan for ~30 hours within a full week to complete a first-time build.

```{tip}
We recommend isolating the build window to within a week and building with no more than two or three individuals in total. This will help reduce the startup cost of picking up where you left off and minimize issues that might come up from poor understanding of the full system. Ideally, all individuals should be involved from the beginning of the process.
```

```{toctree}
:maxdepth: 1
:caption: Prerequisite Knowledge

prerequisite_knowledge
```
```{toctree}
:caption: Part Prep
:maxdepth: 1

heatset_inserts
corner_brackets
```
```{toctree}
:caption: Section 1: Module Assembly
:maxdepth: 1

outer_frame
motor_plate
corner_plate
crossbar
REL
toolchanger_carriage
build_plate
panel
```
```{toctree}
:caption: Section 2: Frame Assembly
:maxdepth: 1

lower_frame
corexy
```
```{toctree}
:caption: Section 3: Final Assembly and Tuning
:maxdepth: 1

z_axis
```

### Videos

In addition to the pdf instructions, we created a [YouTube playlist for certain steps of the build process](https://www.youtube.com/watch?v=8JUbr9aU8eQ) that may be of help.

## Additional Jubilee Resources

- [Jubilee Wiki](https://jubilee3d.com/index.php?title=Main_Page). This is the main documentation hub for the Jubilee project. We encourage you to look through the resources organized on the left-hand sidebar--there's a lot of info there! While not all pages on the wiki will be relevant for lab automation, many help demonstrate Jubilee functionality.
- [Jubilee Discord](https://discord.gg/jubilee). The Jubilee Builders and Extenders Discord is actively used by the Jubilee Community. If you have a question about a build step or troubleshooting your machine, this is a great place to get help! Discussion is organized by topic--you may be interested in the `#lab-automation` channel, for example.
- [Sourcing parts independently](https://jubilee3d.com/index.php?title=Getting_Parts). If you'd prefer to source parts yourselves rather than buy a kit from Filastruder, https://jubilee3d.com has a section with a shopping list and other recommendations.
- [(Original) Jubilee Assembly Instructions](https://jubilee3d.com/index.php?title=Assembly_Instructions). These are the original Jubilee build instructions from which the Science Jubilee build instructions are based on.

## Footnotes
