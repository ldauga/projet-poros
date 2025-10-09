# # from contextlib import redirect_stdout
# # import difflib
# # import math
# # import random
# # import threading
# # import time
# # from typing import Literal, Tuple, Union
# # from minescript import (player, EventQueue, EventType, player_look_at, player_orientation, player_get_targeted_block, player_press_attack, echo, flush, getblock, player_set_orientation, player_press_forward, player_press_right, player_press_left)
# # import sys
# # import json




# # STOP_KEY = 333

# # def kill_process(stop_event: threading.Event):
# #     with EventQueue() as event_queue:
# #         event_queue.register_key_listener()
# #         # event_queue.register_mouse_listener()
# #         while not stop_event.is_set():
# #             event = event_queue.get()
# #             # if event.type == EventType.MOUSE and event.action and not event.button :
# #             #     stop_event.set()
# #             #     break
# #             if event.type == EventType.KEY and event.action == 1:  # key down
# #                 if event.key == STOP_KEY:
# #                     stop_event.set()
# #                     break


# # def point_in_direction(start_pos, orientation, length):
# #     """
# #     Compute the 3D position of a point given a starting position, an orientation, and a distance.
    
# #     start_pos:   (x, y, z) tuple of starting position
# #     orientation: (yaw, pitch) in degrees
# #     length:      distance from starting point
# #     """
# #     x, y, z = start_pos
# #     yaw, pitch = orientation

# #     # Convert to radians
# #     yaw_rad = math.radians(yaw)
# #     pitch_rad = math.radians(pitch)

# #     # Compute directional vector
# #     dx = -math.sin(yaw_rad) * math.cos(pitch_rad)
# #     dy = -math.sin(pitch_rad)
# #     dz =  math.cos(yaw_rad) * math.cos(pitch_rad)

# #     # Scale by length and add to start position
# #     return (
# #         x + dx * length,
# #         y + dy * length,
# #         z + dz * length
# #     )

# # def main(stop_event):
# #     positions = []
    
# #     try:
# #         # player_press_forward(True)
# #         while not stop_event.is_set():
# #             pos = player().position
# #             pos[1]+=1.5
# #             orientation = player_orientation()
# #             ray_end_pos = point_in_direction(pos, orientation, 1)
# #             print(ray_end_pos)
# #             # f.write(f"({ray_end_pos[0]}, {ray_end_pos[1]}, {ray_end_pos[2]})\n")
# #             time.sleep(.2)
# #     finally:
# #         player_press_forward(False)
# #         # with open(sys.path[0] + "/eden.path", "r+") as f:
# #         #     f.seek(0)
# #         #     f.write("\n".join([f'({pos[0]}, {pos[1]}, {pos[2]})' for pos in positions]))
        
        
            
        
        
        



# # if __name__ == "__main__":
# #     stop_event = threading.Event()

# #     t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
# #     t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)
# #     # t3 = threading.Thread(target=avast, args=(stop_event,), daemon=True)

# #     t1.start()
# #     t2.start()
# #     # t3.start()

# #     # Optionally wait for threads to finish
# #     t1.join()
# #     t2.join()
# #     # t3.join()


# import re
# from system.lib.minescript import player_inventory



# POSSIBLE_TOOL = [
#     "minecraft:diamond_hoe",
#     "minecraft:diamond_pickaxe",
# ]


# tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)

# def get_prestige_level(itemstack):
#     match = re.search(r',"text":"(\d+)"}\],"text":"Prestige: "', itemstack.nbt)
#     return int(match.group(1)) if match else None

# print(get_prestige_level(tool))
# # print(tool)

import os, sys, time, wave, contextlib, ctypes
import winsound

# def print_header(wav_path):
#     try:
#         with contextlib.closing(wave.open(wav_path, 'rb')) as wf:
#             nch, sampwidth, fr, nframes, comptype, compname = wf.getnchannels(), wf.getsampwidth(), wf.getframerate(), wf.getnframes(), wf.getcomptype(), wf.getcompname()
#             dur = nframes / float(fr) if fr else 0
#         print(f"[WAV] channels={nch} width={sampwidth*8}bit rate={fr}Hz frames={nframes} duration≈{dur:.2f}s comp={comptype}/{compname}")
#     except Exception as e:
#         print("[WAV] Could not read header:", e)

# def mci(cmd):
#     buf = ctypes.create_unicode_buffer(1024)
#     r = ctypes.windll.winmm.mciSendStringW(cmd, buf, 1024, 0)
#     return r, buf.value

# def play_via_mci(path):
#     # Use a unique alias; quote the path
#     alias = "snd1"
#     r,_ = mci(f'open "{path}" type waveaudio alias {alias}')
#     if r != 0:
#         print(f"[MCI] open failed code={r}")
#         return False
#     r,_ = mci(f'play {alias} wait')
#     if r != 0:
#         print(f"[MCI] play failed code={r}")
#         mci(f'close {alias}')
#         return False
#     mci(f'close {alias}')
#     return True

# print("ding start")

# base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
# wav_path = os.path.join(base_dir, "ding.wav")
# print("Path:", wav_path, "| exists:", os.path.exists(wav_path))

# print_header(wav_path)

# 1) Try a quick Beep as a device sanity check (doesn't use system sound scheme)
import os, sys, time, ctypes

import winsound
winsound.MessageBeep(winsound.MB_OK)
# # 2) Try system alias but don't crash if it fails
# try:
#     print("[Alias] Playing SystemAsterisk (may fail if scheme/perm/device)…")
#     winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
#     print("[Alias] OK")
# except RuntimeError as e:
#     print("[Alias] Failed:", e)

# # 3) Try WAV synchronously
# try:
#     print("[winsound] Playing WAV sync…")
#     winsound.PlaySound(wav_path, winsound.SND_FILENAME)
#     print("[winsound] Sync OK")
# except RuntimeError as e:
#     print("[winsound] Sync failed:", e)

# # 4) Try WAV async for 2s
# try:
#     print("[winsound] Playing WAV async for 2s…")
#     winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
#     time.sleep(2.0)
#     winsound.PlaySound(None, winsound.SND_PURGE)
#     print("[winsound] Async OK (or at least didn’t error)")
# except RuntimeError as e:
#     print("[winsound] Async failed:", e)

# # 5) Fallback: MCI
# print("[MCI] Trying MCI fallback…")
# if play_via_mci(wav_path):
#     print("[MCI] Played successfully.")
# else:
#     print("[MCI] Fallback failed.")

print("ding complete")
