"""Video Sequence Editor (VSE) helpers."""

from __future__ import annotations

import bpy


def get_sequencer_info():
    scene = bpy.context.scene
    sed = scene.sequence_editor
    if not sed:
        scene.sequence_editor_create()
        sed = scene.sequence_editor
    strips = []
    for s in sed.sequences_all if hasattr(sed, "sequences_all") else sed.sequences:
        strips.append({
            "name": s.name,
            "type": s.type,
            "channel": s.channel,
            "frame_start": s.frame_start,
            "frame_final_duration": getattr(s, "frame_final_duration", None),
        })
    return {"strip_count": len(strips), "strips": strips}


def add_movie_strip(filepath, channel=1, frame_start=1, name=None):
    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    sed = scene.sequence_editor
    strip = sed.sequences.new_movie(
        name=name or "Movie",
        filepath=filepath,
        channel=channel,
        frame_start=frame_start,
    )
    return {"name": strip.name, "type": strip.type, "channel": channel}


def add_image_strip(filepath, channel=1, frame_start=1, frame_duration=25, name=None):
    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    sed = scene.sequence_editor
    strip = sed.sequences.new_image(
        name=name or "Image",
        filepath=filepath,
        channel=channel,
        frame_start=frame_start,
    )
    strip.frame_final_duration = frame_duration
    return {"name": strip.name, "duration": frame_duration}


def add_sound_strip(filepath, channel=1, frame_start=1, name=None):
    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    sed = scene.sequence_editor
    strip = sed.sequences.new_sound(
        name=name or "Sound",
        filepath=filepath,
        channel=channel,
        frame_start=frame_start,
    )
    return {"name": strip.name, "type": "SOUND"}


def remove_strip(strip_name):
    scene = bpy.context.scene
    sed = scene.sequence_editor
    if not sed:
        return {"error": "No sequence editor"}
    strip = sed.sequences.get(strip_name)
    if not strip:
        return {"error": f"Strip '{strip_name}' not found"}
    sed.sequences.remove(strip)
    return {"removed": strip_name}


HANDLERS = {
    "get_sequencer_info": get_sequencer_info,
    "add_movie_strip": add_movie_strip,
    "add_image_strip": add_image_strip,
    "add_sound_strip": add_sound_strip,
    "remove_strip": remove_strip,
}
