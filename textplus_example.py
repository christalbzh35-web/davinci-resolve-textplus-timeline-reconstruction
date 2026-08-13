# textplus_example.py
"""

Purpose:
- start from a "carrier" already present on the timeline;
- use a genuine native Text+ source from the Media Pool (MediaPoolItem);
- replace the carrier with a native Text+ at the same timeline position;
- copy the main Fusion/TextPlus parameters.

"Carrier" is a project term for a temporary placeholder clip, not an official
DaVinci Resolve API object.

Preconditions:
- the script runs in a DaVinci Resolve scripting context;
- a timeline is active;
- `template` is the MediaPoolItem of a native Text+ source;
- the carrier contains a Fusion TextPlus node whose inputs are used as source data.

This extract intentionally omits IMS orchestration, reporting, and .drb creation/adaptation.
"""

COPY_INPUTS = (
    "StyledText", "Size", "Center", "Font", "Style", "FontStyle",
    "Red1", "Green1", "Blue1", "Alpha1", "CharacterSpacing",
    "LayoutRotation", "TransformRotation", "SelectTransform",
)


def textplus_tool(timeline_item):
    """Return the first Fusion TextPlus node found on a TimelineItem."""
    try:
        count = int(timeline_item.GetFusionCompCount() or 0)
    except Exception:
        count = 0

    for index in range(1, count + 1):
        comp = timeline_item.GetFusionCompByIndex(index)
        if not comp:
            continue
        for tool in (comp.GetToolList() or {}).values():
            try:
                if tool.GetID() == "TextPlus":
                    return tool
            except Exception:
                pass
    return None


def snapshot_textplus(carrier):
    """Capture carrier timing and TextPlus inputs before replacement."""
    tool = textplus_tool(carrier)
    if not tool:
        raise RuntimeError("Carrier has no usable Fusion TextPlus node.")

    style = {}
    for key in COPY_INPUTS:
        try:
            value = tool.GetInput(key)
        except Exception:
            value = None
        if value is not None:
            style[key] = value

    return {
        "start": int(carrier.GetStart()),
        "duration": int(carrier.GetDuration()),
        "style": style,
    }


def append_native_textplus(media_pool, template, track, start, duration):
    """Insert the native Text+ MediaPoolItem at the carrier position."""
    descriptor = {
        "mediaPoolItem": template,
        "startFrame": 0,
        "endFrame": duration,
        "mediaType": 1,
        "trackIndex": track,
        "recordFrame": start,
    }
    returned = media_pool.AppendToTimeline([descriptor]) or []
    return returned[0] if returned else None


def apply_textplus_style(native_item, style):
    """Copy TextPlus inputs and verify at least StyledText."""
    tool = textplus_tool(native_item)
    if not tool:
        raise RuntimeError("New item does not contain a TextPlus node.")

    for key, value in style.items():
        tool.SetInput(key, value)

    expected = style.get("StyledText")
    if expected is not None and str(tool.GetInput("StyledText")) != str(expected):
        raise RuntimeError("StyledText was not reproduced correctly.")


def replace_carrier_with_textplus(timeline, media_pool, carrier, template, track):
    """
    Core sequence:
    1. snapshot the carrier;
    2. delete it;
    3. insert the Text+ MediaPoolItem at the same start/duration;
    4. copy Fusion parameters;
    5. verify the resulting timeline geometry.
    """
    snap = snapshot_textplus(carrier)

    if not timeline.DeleteClips([carrier], False):
        raise RuntimeError("Resolve refused to delete the carrier.")

    native = append_native_textplus(
        media_pool, template, track, snap["start"], snap["duration"]
    )
    if not native:
        raise RuntimeError("Resolve refused to create the native Text+.")

    if int(native.GetStart()) != snap["start"]:
        raise RuntimeError("Text+ start differs from the carrier start.")
    if int(native.GetDuration()) != snap["duration"]:
        raise RuntimeError(
            "Text+ duration differs from the carrier duration. "
            "Check the Text+ source frame rate against the target timeline."
        )

    apply_textplus_style(native, snap["style"])
    return native
