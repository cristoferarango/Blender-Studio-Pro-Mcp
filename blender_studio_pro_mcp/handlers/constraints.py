"""Object constraints."""

from __future__ import annotations

import bpy

CONSTRAINT_TYPES = [
    "COPY_LOCATION", "COPY_ROTATION", "COPY_SCALE", "COPY_TRANSFORMS",
    "LIMIT_LOCATION", "LIMIT_ROTATION", "LIMIT_SCALE", "LIMIT_DISTANCE",
    "TRACK_TO", "DAMPED_TRACK", "LOCKED_TRACK", "FOLLOW_PATH",
    "CHILD_OF", "FLOOR", "SHRINKWRAP", "CLAMP_TO", "TRANSFORM",
    "ACTION", "ARMATURE", "IK", "SPLINE_IK", "STRETCH_TO", "PIVOT",
]


def add_constraint(object_name, type, name=None, target=None, **params):
    """Add an object constraint. See CONSTRAINT_TYPES."""
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    if type not in CONSTRAINT_TYPES and type not in dir(bpy.types):
        # still try — Blender may support more
        pass
    con = obj.constraints.new(type=type)
    if name:
        con.name = name
    if target:
        tgt = bpy.data.objects.get(target)
        if tgt and hasattr(con, "target"):
            con.target = tgt
    applied = {}
    for k, v in params.items():
        if hasattr(con, k):
            if k in ("target", "space_object") and isinstance(v, str):
                v = bpy.data.objects.get(v)
            try:
                setattr(con, k, v)
                applied[k] = params[k]
            except Exception:
                pass
    return {"object": object_name, "constraint": con.name, "type": con.type, "applied": applied}


def list_constraints(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    return {
        "object": object_name,
        "constraints": [
            {
                "name": c.name,
                "type": c.type,
                "mute": c.mute,
                "target": c.target.name if getattr(c, "target", None) else None,
            }
            for c in obj.constraints
        ],
    }


def remove_constraint(object_name, constraint_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    con = obj.constraints.get(constraint_name)
    if not con:
        return {"error": f"Constraint '{constraint_name}' not found"}
    obj.constraints.remove(con)
    return {"removed": constraint_name}


def set_constraint_param(object_name, constraint_name, param, value):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    con = obj.constraints.get(constraint_name)
    if not con:
        return {"error": f"Constraint '{constraint_name}' not found"}
    if param in ("target", "space_object") and isinstance(value, str):
        value = bpy.data.objects.get(value)
    setattr(con, param, value)
    return {"object": object_name, "constraint": constraint_name, "param": param}


HANDLERS = {
    "add_constraint": add_constraint,
    "list_constraints": list_constraints,
    "remove_constraint": remove_constraint,
    "set_constraint_param": set_constraint_param,
}
