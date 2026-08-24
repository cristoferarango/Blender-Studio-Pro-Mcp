"""Viewport, shading, cursor, and camera view helpers."""

from __future__ import annotations

import bpy


def set_viewport_shading(shading_type="SOLID"):
    """shading_type: WIREFRAME, SOLID, MATERIAL, RENDERED"""
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = shading_type
                    return {"shading": shading_type}
    return {"error": "No VIEW_3D area found", "hint": "Works when Blender UI is open"}


def set_3d_cursor(location=(0, 0, 0), rotation=None):
    cursor = bpy.context.scene.cursor
    cursor.location = location
    if rotation is not None:
        cursor.rotation_euler = rotation
    return {"location": list(cursor.location)}


def get_3d_cursor():
    cursor = bpy.context.scene.cursor
    return {
        "location": list(cursor.location),
        "rotation_euler": list(cursor.rotation_euler),
    }


def snap_cursor_to_selected():
    try:
        bpy.ops.view3d.snap_cursor_to_selected()
        return get_3d_cursor()
    except Exception as e:
        return {"error": str(e)}


def snap_selected_to_cursor(offset=False):
    try:
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=offset)
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


def frame_all():
    try:
        bpy.ops.view3d.view_all()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e), "hint": "Requires VIEW_3D context"}


def frame_selected():
    try:
        bpy.ops.view3d.view_selected()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


def set_pivot_point(type="MEDIAN_POINT"):
    """ACTIVE_ELEMENT, MEDIAN_POINT, INDIVIDUAL_ORIGINS, CURSOR, BOUNDING_BOX_CENTER"""
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    try:
                        bpy.context.scene.tool_settings.transform_pivot_point = type
                    except Exception:
                        space.pivot_point = type
                    return {"pivot": type}
    bpy.context.scene.tool_settings.transform_pivot_point = type
    return {"pivot": type}


HANDLERS = {
    "set_viewport_shading": set_viewport_shading,
    "set_3d_cursor": set_3d_cursor,
    "get_3d_cursor": get_3d_cursor,
    "snap_cursor_to_selected": snap_cursor_to_selected,
    "snap_selected_to_cursor": snap_selected_to_cursor,
    "frame_all": frame_all,
    "frame_selected": frame_selected,
    "set_pivot_point": set_pivot_point,
}
