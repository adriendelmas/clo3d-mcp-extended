"""Static check, no CLO3D needed. Run it after every change to the plugin or the tools.

  python tests/check_static.py

Checks: plugin and server syntax, plugin is ASCII only, every MCP tool sends a command the plugin knows,
every plugin command has a handler and a tool, no duplicate tool names.
"""
import ast
import glob
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PLUGIN = os.path.join(ROOT, "plugin", "clo3d_mcp_plugin.py")
SERVER = [os.path.join(ROOT, "src", "clo3d_mcp", "server.py")] + sorted(
    glob.glob(os.path.join(ROOT, "src", "clo3d_mcp", "extended", "*.py")))
NO_TOOL = {"ping", "stop"}  # listener control only

errors = []


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


plugin = read(PLUGIN)
defined = {n.name for n in ast.parse(plugin).body if isinstance(n, ast.FunctionDef)}
registry = dict(re.findall(r'^\s+"(\w+)": (handle_\w+),', plugin, re.M))
for command, handler in registry.items():
    if handler not in defined:
        errors.append(f"plugin: command {command} points to undefined {handler}")
for number, line in enumerate(plugin.splitlines(), 1):
    if any(ord(c) > 127 for c in line):
        errors.append(f"plugin: non-ASCII character on line {number}")

sent, tools = {}, {}
for path in SERVER:
    text = read(path)
    short = os.path.relpath(path, ROOT)
    for node in ast.parse(text).body:
        if isinstance(node, ast.FunctionDef) and any("tool" in ast.unparse(d) for d in node.decorator_list):
            if node.name in tools:
                errors.append(f"duplicate tool: {node.name} ({tools[node.name]} and {short})")
            tools[node.name] = short
    for command in re.findall(r'_send\(\s*"(\w+)"', text):
        sent.setdefault(command, short)

for command, where in sorted(sent.items()):
    if command not in registry:
        errors.append(f"server: {where} sends {command}, unknown to the plugin")
for command in sorted(set(registry) - set(sent) - NO_TOOL):
    errors.append(f"plugin: command {command} has no MCP tool")

print(f"{len(registry)} plugin commands, {len(tools)} MCP tools, {len(sent)} commands sent")
if errors:
    print("\n".join("  !! " + e for e in errors))
    sys.exit(1)
print("Static check: OK")
