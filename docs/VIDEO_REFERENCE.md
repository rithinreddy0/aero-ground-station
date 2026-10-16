# Basement Creations reference and adaptation notes

Reviewed 10 October 2026 for Aero Ground Station. This incorporates useful setup information into the existing hardware workflow; it does not establish that our aircraft or radio has been tested.

## Sources and local files

- [Video: Building a sub 250g Autonomous Drone with Ardupilot and ExpressLRS AirPort Telemetry](https://www.youtube.com/watch?v=u_ArriXbrR0), published 13 July 2024.
- The expanded description links to the creator's [Printables profile](https://www.printables.com/@Basement_Creations/models) and [Thingiverse profile](https://www.thingiverse.com/basement_creations/designs). No ChatGPT share link was present in the description inspected.
- [Original Thingiverse project and files](https://www.thingiverse.com/thing:6699961/files). Printables' model page was blocked by a browser security verification screen; Thingiverse supplied the bundle.
- [Creator's additional notes](https://github.com/EndlC/BoulderDrone/wiki/Readme).
- Local original bundle: [creator-files.zip](references/basement-creations/creator-files.zip). Its README and LICENSE are preserved inside. Attribution: Basement_Creations; CC BY-NC-SA, with the source page linking to version 4.0. Preserve the original license when reusing its designs.
- [Setup guide](references/basement-creations/Arducopter_Basic_Setup_Guide.pdf), downloaded separately, text extracted and its complete single page visually checked.
- [Wiring illustration](references/basement-creations/images/9e50b286-3637-4c1d-947a-3f970109ece8.png), visually inspected. It is for the creator's F405 Mini and two receivers.

The archive contains ten supplied files: the PDF, Carbon_Frame in STL/STEP, Sub250g_Drone_Frames in F3D/STEP, Flat_Carbon_Frame_160mm.3mf, Test_Frame_nr.1_200mm.3mf, Test_Frame_nr.2_180mm.3mf, Test_Frame_nr.3_160mm.3mf, and LED_Ring_Stack_Cover.3mf. Twelve images include the wiring diagram, frame renders and assembled aircraft. There is no standalone .param file in this Thingiverse bundle. CAD files were inventoried, not dimensionally validated for our build.

## What carries over to this project

The useful sequence is aircraft assembly and ESC checks, correct ArduCopter firmware, sensor/radio calibration, motor mapping, failsafes, initial manual flight validation, telemetry, then missions and Guided operation. This aligns with [COMMISSIONING.md](COMMISSIONING.md). The video chapter list provides useful navigation: flashing 5:40, ArduPilot configuration 8:00, AirPort 14:20, ground station 17:37, missions 18:15, fence 22:16, Guided 24:07. These are description timestamps, not a claim that the entire video was watched or transcribed.

The creator uses a SpeedyBee F405 Mini 35A stack, a Walksnail GPS, separate telemetry/RC receivers and a small 3S build. Our recorded board is SPEEDYBEEF405AIO and handset is RadioMaster Pocket. The small frame files may be useful design references, but their mounting, clearance and mass need checking against our components. The creator prefers carbon PETG/PA12 and reports limitations with motor loading and low-voltage ESC operation; those are observations about his build, not measurements of ours.

## Settings that require adaptation

The supplied PDF assumes GPS on SERIAL6 and conventional RC on SERIAL2. It also gives orientation, RC option bits, switch assignments, DShot600 and initial tuning assumptions for a 3-inch, 3S Li-ion aircraft. Treat all these as donor settings. Recompute battery/tune settings from our actual pack and propellers, verify installed FC orientation and motor order, and select channel options from the installed firmware documentation. A complete parameter import is inappropriate for this different board.

[Official AIO documentation](https://ardupilot.org/copter/docs/common-speedybeef405aio.html) instead maps GPS to SERIAL5 and DMA-enabled RC to SERIAL6; SERIAL2 is inverted receive-only. Bidirectional receiver wiring needs both RX and TX, so the PDF's SERIAL2 assignment cannot be transferred to this AIO. The AIO has no internal compass. Verify our GPS/compass identity and firmware target before adapting the illustration. Board-specific firmware is SpeedyBeeF405AIO; initial DFU uses with_bl.hex and subsequent updates use .apj. A board's voltage sensor range does not establish the integrated ESC's allowed input range.

## AirPort versus the intended telemetry link

[Official AirPort guidance](https://www.expresslrs.org/software/airport/) now recommends native MAVLink instead. AirPort replaces RC with transparent serial data, so the video requires a second radio pair for manual control. Its serial rate must fit RF throughput; do not reuse the video's rate for native MAVLink. It has no transport acknowledgement/retransmission.

[Current ExpressLRS MAVLink guidance](https://www.expresslrs.org/software/mavlink/) supports RC and telemetry over one compatible ESP-based pair. Minimum TX/RX firmware is 3.5.0, with Backpack 1.5.0 for Wi-Fi forwarding. Internal modules require Backpack Wi-Fi for the GCS; a Pocket handset USB connection is not that endpoint. Confirm the Pocket's actual Backpack hardware. A compatible external module can provide USB serial.

For the selected FC UART, the documented native ArduPilot settings are protocol 2, baud 460 and RSSI type 5. Reduce corresponding stream groups as documented, keeping ADSB/PARAMS/RAW_CTRL at zero. Firmware v3 needs explicit RX MAVLink selection; v4 configures it automatically from TX link mode. Backpack Telemetry=WiFi enables forwarding; firmware-update Wi-Fi does not. UDP reception uses port 14550. These remain commissioning instructions, not settings applied to a connected vehicle.

## Consequences for our software

Keep the current serial/UDP MAVLink adapter and default-disabled live control. Begin with live observation, using one GCS per endpoint or a configured router. Check GPS, heading, battery and message freshness, then prove takeover and link-loss handling under the existing commissioning procedure.

The video's autonomous flight is a reference for ArduPilot operation. Our existing missions run in the laptop controller using Guided setpoints; they are not onboard AUTO mission uploads. Mission upload/download with acknowledgements remains on [ROADMAP.md](ROADMAP.md). The reference supplies no person-detection model, capture-card latency measurements, obstacle avoidance or victim geolocation method. Those project gaps remain unchanged.

Next information needed is the exact receiver, ELRS TX/RX versions, Pocket Backpack capability, GPS/compass model, battery/propellers, and video receiver AV output. Until those are identified, this reference improves our integration plan but cannot resolve exact wiring or flight settings.
