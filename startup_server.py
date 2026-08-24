"""Auto-start script for Blender Studio Pro MCP.
Author: Cristofer Arango — https://corporacionarango.com
License: Apache-2.0

Usage: blender --python /path/to/startup_server.py
"""
import bpy

def _delayed_start():
    """Start server after Blender is fully initialized."""
    bpy.ops.preferences.addon_enable(module="blender_studio_pro_mcp")
    bpy.ops.bmpro.start_server()
    print("Blender Studio Pro MCP: Server started on port 9877")
    print("Cristofer Arango / https://corporacionarango.com")
    return None

bpy.app.timers.register(_delayed_start, first_interval=2.0)
print("Blender Studio Pro MCP: Server will auto-start in 2 seconds...")
