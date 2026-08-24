"""Static map of Blender bpy.ops categories (from official API docs).

At runtime, list_operator_categories() returns the live set for the installed Blender.
This file documents the expected ~70 categories for agents and docs.
"""

BLENDER_OPS_CATEGORIES = [
    "action", "anim", "armature", "asset", "boid", "brush", "buttons",
    "cachefile", "camera", "clip", "cloth", "collection", "console",
    "constraint", "curve", "curves", "cycles", "dpaint", "ed",
    "export_anim", "export_scene", "extensions", "file", "fluid", "font",
    "geometry", "gizmogroup", "gpencil", "graph", "grease_pencil", "image",
    "import_anim", "import_curve", "import_scene", "info", "lattice",
    "marker", "mask", "material", "mball", "mesh", "nla", "node", "object",
    "outliner", "paint", "paintcurve", "palette", "particle", "pointcloud",
    "pose", "poselib", "preferences", "ptcache", "render", "rigidbody",
    "scene", "screen", "script", "sculpt", "sculpt_curves", "sequencer",
    "sound", "spreadsheet", "surface", "text", "text_editor", "texture",
    "transform", "ui", "uilist", "uv", "view2d", "view3d", "wm",
    "workspace", "world",
]

# Approx operator counts vary by Blender version; 4.x/5.x typically 1500–2500+ ops.
EXPECTED_CATEGORY_COUNT = len(BLENDER_OPS_CATEGORIES)
