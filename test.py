# # Minescript v4.0 – read TAB header/footer to detect subserver

# import re
# from minescript import (
#     echo, version_info, world_info,
#     java_class, java_member, java_call_method, java_access_field, java_to_string
# )

# # patterns you expect in the TAB header/footer
# PATTERNS = [
#     r"\b([a-z][a-z0-9_\-]+-[a-f0-9]{6,})\b",                  # island-0fd381lab
#     r"\b(server|realm|shard)\s*[:=]\s*([a-z0-9_\-\.]+)\b",     # Server: island-01
#     r"\bconnected to\s+([a-z0-9_\-\.]+)\b",                    # connected to island
# ]

# def _first_match(text: str):
#     if not text:
#         return None
#     low = text.lower()
#     for pat in PATTERNS:
#         m = re.search(pat, low)
#         if m:
#             # pick the last non-empty capturing group
#             for g in reversed(m.groups()):
#                 if g:
#                     return g
#     return None

# def get_tab_text():
#     """
#     Returns (header_text, footer_text) from the player list (TAB).
#     Works with Mojang mappings (classes/members by name).
#     """
#     # Minecraft singleton
#     MC = java_class("net.minecraft.client.Minecraft")
#     mc = java_call_method(MC, java_member(MC, "getInstance"))

#     # gui instance
#     GUI = java_class("net.minecraft.client.gui.Gui")
#     gui = java_access_field(mc, java_member(MC, "gui"))  # Minecraft.gui

#     # PlayerTabOverlay
#     PTO = java_class("net.minecraft.client.gui.components.PlayerTabOverlay")
#     tab = java_call_method(gui, java_member(GUI, "getTabList"))

#     # header/footer are Components; prefer getString() over toString()
#     COMP = java_class("net.minecraft.network.chat.Component")
#     getString = java_member(COMP, "getString")

#     header_comp = java_access_field(tab, java_member(PTO, "header"))
#     footer_comp = java_access_field(tab, java_member(PTO, "footer"))

#     header = java_call_method(header_comp, getString) if header_comp else None
#     footer = java_call_method(footer_comp, getString) if footer_comp else None

#     # Fallback if getString() unavailable
#     if header is None and header_comp:
#         header = java_to_string(header_comp)
#     if footer is None and footer_comp:
#         footer = java_to_string(footer_comp)

#     return (header or ""), (footer or "")

# def detect_subserver():
#     # try:
#         header, footer = get_tab_text()
#         print(header, footer)
#         name = _first_match(header) or _first_match(footer)
#         if name:
#             return name
#     # except Exception as e:
#     #     # If mappings are obfuscated or classes differ, we’ll fall back.
#     #     pass

#     # Last-resort: proxy entry info (often not the subserver, but better than nothing)
#     # wi = world_info()
#     # return wi.name or wi.address

# sub = detect_subserver()
# echo("Current subserver:", sub if sub else "unknown")

print("""
__   _  __  __   __ 
|__)/  \\|__)/   \\ /__`
|    \\_/ |  \\\\__/ .__/
""")



# play_mp3(os.path.join(sys.path[0], "bing.mp3"))

# print("finish")

