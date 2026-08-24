"""Mesh edit-mode operations."""

from __future__ import annotations

import bpy
import bmesh


def enter_edit_mode(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    return {"object": object_name, "mode": "EDIT"}


def mesh_select_all(action="SELECT"):
    """action: SELECT, DESELECT, TOGGLE, INVERT"""
    bpy.ops.mesh.select_all(action=action)
    return {"action": action}


def subdivide(number_cuts=1, smoothness=0.0):
    bpy.ops.mesh.subdivide(number_cuts=number_cuts, smoothness=smoothness)
    return {"number_cuts": number_cuts, "smoothness": smoothness}


def extrude_region(value=1.0):
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, value)}
    )
    return {"value": value}


def inset_faces(thickness=0.1, depth=0.0):
    bpy.ops.mesh.inset(thickness=thickness, depth=depth)
    return {"thickness": thickness, "depth": depth}


def bevel(offset=0.1, segments=1):
    bpy.ops.mesh.bevel(offset=offset, segments=segments)
    return {"offset": offset, "segments": segments}


def loop_cut(number_cuts=1, edge_index=None):
    """Loop cut — best effort; may need viewport context."""
    try:
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": number_cuts})
        return {"number_cuts": number_cuts}
    except Exception as e:
        return {
            "error": str(e),
            "hint": "Use call_operator('mesh.loopcut_slide', ...) or execute_python with bmesh.",
        }


def delete_geometry(type="VERT"):
    """type: VERT, EDGE, FACE, ONLY_FACE, EDGE_FACE"""
    bpy.ops.mesh.delete(type=type)
    return {"deleted": type}


def merge_by_distance(threshold=0.0001):
    bpy.ops.mesh.remove_doubles(threshold=threshold)
    return {"threshold": threshold}


def get_mesh_stats(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    mesh = obj.data
    return {
        "object": object_name,
        "vertices": len(mesh.vertices),
        "edges": len(mesh.edges),
        "polygons": len(mesh.polygons),
    }


def apply_bmesh_op(object_name, operation="recalc_normals"):
    """Run a simple bmesh operation: recalc_normals, triangulate, remove_doubles."""
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    was_edit = obj.mode == "EDIT"
    if was_edit:
        bm = bmesh.from_edit_mesh(obj.data)
    else:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
    if operation == "recalc_normals":
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    elif operation == "triangulate":
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
    elif operation == "remove_doubles":
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0001)
    else:
        return {"error": f"Unknown operation: {operation}"}
    if was_edit:
        bmesh.update_edit_mesh(obj.data)
    else:
        bm.to_mesh(obj.data)
        bm.free()
    return {"object": object_name, "operation": operation}


HANDLERS = {
    "enter_edit_mode": enter_edit_mode,
    "mesh_select_all": mesh_select_all,
    "subdivide": subdivide,
    "extrude_region": extrude_region,
    "inset_faces": inset_faces,
    "bevel": bevel,
    "loop_cut": loop_cut,
    "delete_geometry": delete_geometry,
    "merge_by_distance": merge_by_distance,
    "get_mesh_stats": get_mesh_stats,
    "apply_bmesh_op": apply_bmesh_op,
}
