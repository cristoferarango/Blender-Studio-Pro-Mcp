"""Universal Blender bridge — 100% bpy.ops coverage for Blender Studio Pro MCP.

Any Blender operator in any category can be discovered, inspected, polled, and
invoked (with optional context override). This is the complete-access layer used
by Cursor, Claude, Codex, OpenCode, DeepSeek, and any MCP client.
"""

from __future__ import annotations

import bpy


def _normalize_idname(idname: str) -> str:
    """Accept 'mesh.subdivide' or 'MESH_OT_subdivide'."""
    idname = (idname or "").strip()
    if "_OT_" in idname:
        left, right = idname.split("_OT_", 1)
        return f"{left.lower()}.{right.lower()}"
    return idname


def _get_op(idname: str):
    idname = _normalize_idname(idname)
    if "." not in idname:
        return None, None, idname, "idname must look like 'module.operator'"
    mod_name, op_name = idname.split(".", 1)
    mod = getattr(bpy.ops, mod_name, None)
    if mod is None:
        return None, None, idname, f"Unknown category: {mod_name}"
    op = getattr(mod, op_name, None)
    if op is None:
        return None, None, idname, f"Unknown operator: {idname}"
    return op, mod_name, idname, None


def _view3d_override():
    """Build a context override dict for VIEW_3D when available."""
    wm = bpy.context.window_manager
    for window in wm.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for region in area.regions:
                if region.type == "WINDOW":
                    return {
                        "window": window,
                        "screen": screen,
                        "area": area,
                        "region": region,
                        "scene": bpy.context.scene,
                        "view_layer": bpy.context.view_layer,
                    }
    return None


def list_operator_categories():
    """List every bpy.ops submodule available in this Blender build (100% live)."""
    cats = []
    for name in sorted(dir(bpy.ops)):
        if name.startswith("_"):
            continue
        mod = getattr(bpy.ops, name)
        try:
            count = len([o for o in dir(mod) if not o.startswith("_")])
        except Exception:
            count = 0
        cats.append({"category": name, "operator_count": count})
    return {
        "app": "Blender Studio Pro MCP",
        "categories": cats,
        "total_categories": len(cats),
        "total_operators": sum(c["operator_count"] for c in cats),
        "blender_version": bpy.app.version_string,
        "coverage": "100% of bpy.ops via call_operator",
    }


def list_operators(category=None, search=None, limit=500):
    """List operators (live). Filter by category and/or search. Default limit 500."""
    results = []
    mods = [category] if category else [n for n in dir(bpy.ops) if not n.startswith("_")]
    search_l = (search or "").lower()

    for mod_name in mods:
        mod = getattr(bpy.ops, mod_name, None)
        if mod is None:
            return {"error": f"Unknown operator category: {category}"}
        for op_name in sorted(dir(mod)):
            if op_name.startswith("_"):
                continue
            idname = f"{mod_name}.{op_name}"
            if search_l and search_l not in idname.lower():
                continue
            results.append(idname)
            if len(results) >= limit:
                return {
                    "operators": results,
                    "count": len(results),
                    "truncated": True,
                    "limit": limit,
                }

    return {"operators": results, "count": len(results), "truncated": False}


def search_operators(query, limit=100):
    """Search all categories for operators matching query (substring)."""
    return list_operators(category=None, search=query, limit=limit)


def get_operator_info(idname):
    """Return RNA property schema for any operator."""
    op, _, idname, err = _get_op(idname)
    if err:
        return {"error": err, "idname": idname}

    props = []
    try:
        rna = op.get_rna_type()
        for p in rna.properties:
            if p.identifier in ("rna_type",):
                continue
            entry = {
                "identifier": p.identifier,
                "name": p.name,
                "type": p.type,
                "description": p.description or "",
            }
            if hasattr(p, "default"):
                try:
                    entry["default"] = p.default
                except Exception:
                    pass
            if p.type == "ENUM":
                try:
                    entry["enum_items"] = [i.identifier for i in p.enum_items]
                except Exception:
                    pass
            props.append(entry)
    except Exception as e:
        return {"idname": idname, "error": f"Could not read RNA: {e}"}

    return {"idname": idname, "properties": props, "property_count": len(props)}


def poll_operator(idname):
    """Check whether an operator can run in the current context (poll)."""
    op, _, idname, err = _get_op(idname)
    if err:
        return {"error": err, "idname": idname}
    try:
        can_run = bool(op.poll())
    except Exception as e:
        return {"idname": idname, "poll": False, "error": str(e)}
    return {"idname": idname, "poll": can_run}


def call_operator(
    idname,
    params=None,
    execution_context="EXEC_DEFAULT",
    use_view3d_override=True,
):
    """Call any Blender operator (100% bpy.ops surface).

    Args:
        idname: 'mesh.subdivide' or 'MESH_OT_subdivide'
        params: operator properties dict
        execution_context: EXEC_DEFAULT, INVOKE_DEFAULT, EXEC_SCREEN, ...
        use_view3d_override: retry with VIEW_3D context override on failure
    """
    params = dict(params or {})
    op, _, idname, err = _get_op(idname)
    if err:
        return {"error": err, "idname": idname}

    def _invoke(with_override: bool):
        if with_override:
            ov = _view3d_override()
            if ov is None:
                raise RuntimeError("No VIEW_3D area for context override")
            with bpy.context.temp_override(**ov):
                return op(execution_context, **params)
        return op(execution_context, **params)

    try:
        result = _invoke(False)
        return {
            "idname": idname,
            "result": list(result) if result is not None else ["FINISHED"],
            "params": params,
            "override": False,
        }
    except Exception as first:
        if not use_view3d_override:
            return {
                "error": str(first),
                "idname": idname,
                "hint": "Try get_operator_info / poll_operator / set_mode, or use_view3d_override=true.",
            }
        try:
            result = _invoke(True)
            return {
                "idname": idname,
                "result": list(result) if result is not None else ["FINISHED"],
                "params": params,
                "override": True,
            }
        except Exception as second:
            return {
                "error": str(second),
                "first_error": str(first),
                "idname": idname,
                "hint": "Check mode/selection, get_operator_info(), or execute_python for custom context.",
            }


def call_operators_batch(calls):
    """Run multiple operators in order.

    calls: list of {idname, params?, execution_context?, use_view3d_override?}
    """
    if not isinstance(calls, list):
        return {"error": "calls must be a list of operator call dicts"}
    results = []
    for i, item in enumerate(calls):
        if not isinstance(item, dict) or "idname" not in item:
            results.append({"index": i, "error": "each item needs idname"})
            continue
        r = call_operator(
            item["idname"],
            params=item.get("params"),
            execution_context=item.get("execution_context", "EXEC_DEFAULT"),
            use_view3d_override=item.get("use_view3d_override", True),
        )
        r["index"] = i
        results.append(r)
        if "error" in r:
            return {"status": "stopped_on_error", "results": results}
    return {"status": "ok", "results": results}


def get_coverage_report():
    """Report live Blender coverage for Blender Studio Pro MCP."""
    cats = list_operator_categories()
    dedicated = list_dedicated_commands()
    return {
        "app": "Blender Studio Pro MCP",
        "author": "Cristofer Arango",
        "website": "https://corporacionarango.com",
        "blender_version": cats.get("blender_version"),
        "bpy_ops_categories": cats.get("total_categories"),
        "bpy_ops_operators": cats.get("total_operators"),
        "dedicated_commands": dedicated.get("total") if isinstance(dedicated, dict) else None,
        "dedicated_modules": dedicated.get("modules") if isinstance(dedicated, dict) else None,
        "access": {
            "any_operator": "call_operator / call_operators_batch",
            "discover": "list_operator_categories / list_operators / search_operators",
            "inspect": "get_operator_info / poll_operator",
            "data": "list_data_types / list_data_items / get_attr_path / set_attr_path",
            "python": "execute_python",
        },
        "coverage_percent": 100,
        "clients": ["Cursor", "Claude", "Codex", "OpenCode", "DeepSeek", "Windsurf", "any MCP"],
    }


def list_data_types():
    """List bpy.data collection names (objects, meshes, materials, ...)."""
    names = []
    for name in dir(bpy.data):
        if name.startswith("_"):
            continue
        attr = getattr(bpy.data, name, None)
        if attr is None:
            continue
        if hasattr(attr, "__len__") and hasattr(attr, "__iter__") and not isinstance(attr, (str, bytes)):
            try:
                names.append({"type": name, "count": len(attr)})
            except Exception:
                names.append({"type": name, "count": None})
    return {"data_types": names}


def list_data_items(data_type, limit=200):
    """List item names in a bpy.data collection."""
    coll = getattr(bpy.data, data_type, None)
    if coll is None:
        return {"error": f"Unknown data type: {data_type}"}
    try:
        items = [item.name for item in coll]
    except Exception as e:
        return {"error": str(e)}
    truncated = len(items) > limit
    return {
        "data_type": data_type,
        "items": items[:limit],
        "count": len(items),
        "truncated": truncated,
    }


def get_attr_path(path):
    """Read a value via path, e.g. 'context.scene.frame_current' or 'data.objects[\"Cube\"].location'."""
    try:
        value = _resolve_path(path)
        return {"path": path, "value": _serialize(value)}
    except Exception as e:
        return {"error": str(e), "path": path}


def set_attr_path(path, value):
    """Set a value via dotted path ending in an attribute name."""
    try:
        parent, attr = _resolve_parent(path)
        setattr(parent, attr, value)
        return {"path": path, "value": _serialize(getattr(parent, attr))}
    except Exception as e:
        return {"error": str(e), "path": path}


def get_mode():
    """Return current object interaction mode."""
    obj = bpy.context.object
    return {
        "mode": bpy.context.mode,
        "object": obj.name if obj else None,
        "object_mode": obj.mode if obj else None,
    }


def set_mode(mode, object_name=None):
    """Switch mode: OBJECT, EDIT, SCULPT, POSE, WEIGHT_PAINT, etc."""
    if object_name:
        obj = bpy.data.objects.get(object_name)
        if not obj:
            return {"error": f"Object '{object_name}' not found"}
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
    try:
        bpy.ops.object.mode_set(mode=mode)
        return get_mode()
    except Exception as e:
        return {"error": str(e), "hint": "Some modes require a suitable active object type."}


def get_selection():
    """Return selected object names and active object."""
    active = bpy.context.view_layer.objects.active
    return {
        "selected": [o.name for o in bpy.context.selected_objects],
        "active": active.name if active else None,
    }


def set_selection(object_names, active=None, extend=False):
    """Select objects by name."""
    if not extend:
        bpy.ops.object.select_all(action="DESELECT")
    selected = []
    for name in object_names or []:
        obj = bpy.data.objects.get(name)
        if obj:
            obj.select_set(True)
            selected.append(name)
    if active:
        obj = bpy.data.objects.get(active)
        if obj:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            if active not in selected:
                selected.append(active)
    return get_selection()


def undo():
    """Undo last action."""
    try:
        bpy.ops.ed.undo()
        return {"status": "ok", "action": "undo"}
    except Exception as e:
        return {"error": str(e)}


def redo():
    """Redo last undone action."""
    try:
        bpy.ops.ed.redo()
        return {"status": "ok", "action": "redo"}
    except Exception as e:
        return {"error": str(e)}


def list_tool_categories():
    """High-level dedicated category map + pointer to 100% bpy.ops bridge."""
    return {
        "app": "Blender Studio Pro MCP",
        "note": (
            "100% Blender: list_operator_categories / search_operators / "
            "get_operator_info / poll_operator / call_operator / call_operators_batch "
            "cover every bpy.ops category in your installed Blender."
        ),
        "coverage_percent": 100,
        "dedicated_categories": [
            "bridge", "scene", "objects", "materials", "shader_nodes", "lights",
            "modifiers", "animation", "geometry_nodes", "camera", "render",
            "io", "uv_texture", "batch", "assets", "rigging", "physics",
            "particles", "grease_pencil", "sculpt_paint", "compositor",
            "sequencer", "constraints", "shapekeys", "world", "mesh_edit",
            "curves_text", "viewport", "files", "timeline", "collections",
            "drivers_props", "code_exec",
        ],
    }


def list_dedicated_commands():
    """List all dedicated high-level commands registered in this addon."""
    import sys
    handlers_pkg = sys.modules.get(__name__.rsplit(".", 1)[0])
    if handlers_pkg and hasattr(handlers_pkg, "list_registered_commands"):
        return handlers_pkg.list_registered_commands()
    return {"error": "Handler registry not available"}


def _serialize(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if hasattr(value, "to_list"):
        try:
            return list(value)
        except Exception:
            pass
    if hasattr(value, "[:]"):
        try:
            return list(value[:])
        except Exception:
            pass
    if isinstance(value, (list, tuple)):
        return [_serialize(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize(v) for k, v in value.items()}
    return str(value)


def _resolve_path(path: str):
    ns = {"bpy": bpy, "context": bpy.context, "data": bpy.data}
    expr = path.strip()
    if expr.startswith("bpy."):
        return eval(expr, {"bpy": bpy})
    if expr.startswith("context.") or expr.startswith("data."):
        return eval(expr, ns)
    return eval(f"bpy.{expr}", {"bpy": bpy})


def _resolve_parent(path: str):
    path = path.strip()
    if "." not in path and "[" not in path:
        raise ValueError("Path must include a parent attribute")
    if path.startswith("context.") or path.startswith("data."):
        parent_expr, attr = path.rsplit(".", 1)
        if "[" in attr:
            raise ValueError("Cannot set indexed path this way; use execute_python")
        ns = {"bpy": bpy, "context": bpy.context, "data": bpy.data}
        return eval(parent_expr, ns), attr
    full = path if path.startswith("bpy.") else f"bpy.{path}"
    parent_expr, attr = full.rsplit(".", 1)
    if "[" in attr:
        raise ValueError("Cannot set indexed path this way; use execute_python")
    return eval(parent_expr, {"bpy": bpy}), attr


HANDLERS = {
    "list_operator_categories": list_operator_categories,
    "list_operators": list_operators,
    "search_operators": search_operators,
    "get_operator_info": get_operator_info,
    "poll_operator": poll_operator,
    "call_operator": call_operator,
    "call_operators_batch": call_operators_batch,
    "get_coverage_report": get_coverage_report,
    "list_data_types": list_data_types,
    "list_data_items": list_data_items,
    "get_attr_path": get_attr_path,
    "set_attr_path": set_attr_path,
    "get_mode": get_mode,
    "set_mode": set_mode,
    "get_selection": get_selection,
    "set_selection": set_selection,
    "undo": undo,
    "redo": redo,
    "list_tool_categories": list_tool_categories,
    "list_dedicated_commands": list_dedicated_commands,
}
