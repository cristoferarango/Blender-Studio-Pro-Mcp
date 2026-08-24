"""Enable Blender Studio Pro MCP and optionally start the server."""
import bpy
import addon_utils

MODULE = "blender_studio_pro_mcp"

# Enable addon
addon_utils.enable(MODULE, default_set=True, persistent=True)

# Persist preferences
bpy.ops.wm.save_userpref()
print("ENABLED:", MODULE)

# Verify
loaded = MODULE in bpy.context.preferences.addons.keys()
print("LOADED:", loaded)
