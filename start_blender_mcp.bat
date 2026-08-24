@echo off
REM Start Blender with Blender Studio Pro MCP auto-server
set ADDON_SCRIPT=%~dp0startup_server.py
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --python "%ADDON_SCRIPT%"
