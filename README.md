# Native Text+ and external timeline reconstruction in DaVinci Resolve

This repository accompanies a technical experience report about reconstructing, in DaVinci Resolve, a timeline produced by an external application.

The original use case is **Icare Motion Studio (IMS)**, an in-house automated video-editing application built around Remotion Studio. The complete IMS bridge is not published here; this repository isolates the mechanisms that may be reusable elsewhere.

## Native editable Text+: the core mechanism

The validated sequence is:

**carrier on timeline -> native Text+ MediaPoolItem -> replacement -> Fusion/TextPlus parameters**

A **carrier** is the term used here for a temporary placeholder clip. It defines the target start position and duration; it is not a DaVinci Resolve API object or official term.

`textplus_example.py` is a minimal extract derived from the validated IMS V10 implementation. It shows how to:

1. read timing and TextPlus parameters from a carrier;
2. remove the carrier;
3. insert a genuine Text+ `MediaPoolItem` at the same `recordFrame`, track and duration;
4. copy Fusion/TextPlus inputs;
5. verify the resulting timing.

## Frame-rate pitfall

A Text+ source prepared at 24 fps and used in a 25 fps timeline produced durations close to a 25/24 ratio (for example, 75 requested frames became about 78). The working fix was to make the Text+ source consistent with the target timeline frame rate rather than compensate durations numerically.

## Resolve Free and external control

In the tested environment, the bridge runs **inside Resolve**. The external application and the bridge exchange request/response files. This keeps Resolve API calls in the Resolve process while allowing an external application to orchestrate them.

## Files

- `RETEX_DaVinci_TextPlus_EN.pdf` - full English experience report.
- `textplus_example.py` - minimal validated mechanism.
- `SOURCES.md` - technical references.
- `FORUM_BMD_POST_EN.md` - concise post prepared for the Blackmagic Design forum.
- `RETEX_DaVinci_TextPlus_FR.pdf` - French reference version, if published alongside the English version.

## Tested environment

Windows; DaVinci Resolve 20.3.1 Build 4 and 21.0.2 Build 4.

These are experimental results from the tested environments, not general guarantees from Blackmagic Design.

## License

No reuse license is assigned in this publication kit yet. Choose the intended code/documentation license before publishing the repository.
