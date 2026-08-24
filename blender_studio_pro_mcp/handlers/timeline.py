"""Timeline markers and playback helpers."""

from __future__ import annotations

import bpy


def add_marker(name, frame=None):
    scene = bpy.context.scene
    if frame is None:
        frame = scene.frame_current
    m = scene.timeline_markers.new(name, frame=frame)
    return {"name": m.name, "frame": m.frame}


def list_markers():
    scene = bpy.context.scene
    return {
        "markers": [{"name": m.name, "frame": m.frame} for m in scene.timeline_markers]
    }


def remove_marker(name):
    scene = bpy.context.scene
    m = scene.timeline_markers.get(name)
    if not m:
        return {"error": f"Marker '{name}' not found"}
    scene.timeline_markers.remove(m)
    return {"removed": name}


def play_animation():
    try:
        bpy.ops.screen.animation_play()
        return {"status": "playing"}
    except Exception as e:
        return {"error": str(e)}


def stop_animation():
    try:
        if bpy.context.screen.is_animation_playing:
            bpy.ops.screen.animation_play()
        return {"status": "stopped"}
    except Exception as e:
        return {"error": str(e)}


def set_preview_range(start, end, enabled=True):
    scene = bpy.context.scene
    scene.use_preview_range = enabled
    scene.frame_preview_start = start
    scene.frame_preview_end = end
    return {"start": start, "end": end, "enabled": enabled}


HANDLERS = {
    "add_marker": add_marker,
    "list_markers": list_markers,
    "remove_marker": remove_marker,
    "play_animation": play_animation,
    "stop_animation": stop_animation,
    "set_preview_range": set_preview_range,
}
