

import math
import os
import sys
import threading
from time import sleep
from typing import Tuple
import winsound

import pyautogui

from utils.pygame_loader import play_mp3
from system.lib.minescript import EventQueue, EventType, player, player_inventory, player_orientation, player_position


STOP_KEY = 333
SOUND_RESETER_KEY = 330

def kill_process(stop_event: threading.Event, reset_sound):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if ev and ev.type == EventType.KEY and ev.action == 1:  # key down
                if ev.key == STOP_KEY:
                    print("Stopping")
                    stop_event.set()
                    break
                if ev.key == SOUND_RESETER_KEY:
                    reset_sound[0] = True
                    


def distance_between_points(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """
    Calculate the Euclidean distance between two 3D points.
    
    Args:
        p1 (tuple): First point as (x, y, z).
        p2 (tuple): Second point as (x, y, z).
        
    Returns:
        float: Distance between p1 and p2.
    """
    return abs(math.sqrt((p2[0] - p1[0])**2 +
                     (p2[1] - p1[1])**2 +
                     (p2[2] - p1[2])**2))
import time
import ctypes
from ctypes import wintypes
import win32con
import win32gui
import win32process
import win32api  # still used for keybd_event; fine if present

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# ctypes prototypes
user32.AttachThreadInput.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.BOOL]
user32.AttachThreadInput.restype  = wintypes.BOOL

user32.AllowSetForegroundWindow.argtypes = [wintypes.DWORD]
user32.AllowSetForegroundWindow.restype  = wintypes.BOOL

kernel32.GetCurrentThreadId.argtypes = []
kernel32.GetCurrentThreadId.restype  = wintypes.DWORD

ASFW_ANY = 0xFFFFFFFF

def _allow_set_foreground_window_any():
    try:
        user32.AllowSetForegroundWindow(ASFW_ANY)
    except Exception:
        pass  # non-fatal

def _get_current_tid() -> int:
    return int(kernel32.GetCurrentThreadId())

def _attach_thread_input(src_tid: int, dst_tid: int, attach: bool) -> bool:
    return bool(user32.AttachThreadInput(src_tid, dst_tid, attach))

def _get_root(hwnd):
    GA_ROOT = 2
    try:
        return win32gui.GetAncestor(hwnd, GA_ROOT)
    except win32gui.error:
        return hwnd

def _likely_mc_title(title: str) -> bool:
    t = title.lower()
    return any(n in t for n in ("minecraft", "lwjgl", "glfw"))

def _enum_top_windows():
    hwnds = []
    def enum_handler(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if title and _likely_mc_title(title):
            hwnds.append(_get_root(hwnd))
    win32gui.EnumWindows(enum_handler, None)
    # dedup while preserving order
    seen = set(); out = []
    for h in hwnds:
        if h not in seen:
            seen.add(h); out.append(h)
    return out

def _force_foreground(hwnd) -> bool:
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.05)

    fg = win32gui.GetForegroundWindow()
    if fg == hwnd:
        return True

    _allow_set_foreground_window_any()

    try:
        fg_tid = win32process.GetWindowThreadProcessId(fg)[0] if fg else 0
        this_tid = _get_current_tid()
        attached = False
        if fg_tid and fg_tid != this_tid:
            attached = _attach_thread_input(fg_tid, this_tid, True)

        try:
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetActiveWindow(hwnd)
            win32gui.SetForegroundWindow(hwnd)
        finally:
            if attached:
                _attach_thread_input(fg_tid, this_tid, False)
    except win32gui.error:
        # ALT nudge fallback
        try:
            win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
            win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.02)
            win32gui.SetForegroundWindow(hwnd)
        except win32gui.error:
            return False

    return win32gui.GetForegroundWindow() == hwnd

def focus_minecraft():
    hwnds = _enum_top_windows()
    print(hwnds)
    if not hwnds:
        print("Minecraft window not found.")
        return False

    hwnd = hwnds[0]
    title = win32gui.GetWindowText(hwnd)
    ok = _force_foreground(hwnd)
    if ok:
        print(f"Focused Minecraft window: {title}")
    else:
        print(f"Could not focus window: {title}")
    return ok



POSSIBLE_TOOL = [
    "minecraft:diamond_hoe",
    "minecraft:diamond_pickaxe",
]

def main(stop_event: threading.Event, reset_sound):

    check = False 
    
    last_pos = player_position()
    last_yaw, last_pitch = player_orientation()
    last_tool = next(
        (item for item in player_inventory() if item.item in POSSIBLE_TOOL),
        None,
    )
    
    while not stop_event.is_set():
        
        if reset_sound[0]:
            check = False
            reset_sound[0] = False
        
        if check:
            play_mp3(os.path.join(sys.path[0], "assets/alarm.mp3"))

        yaw, pitch = player_orientation()
        pos = player_position()
        tool = next(
            (item for item in player_inventory() if item.item in POSSIBLE_TOOL),
            None,
        )
        
        if distance_between_points(last_pos, pos) > 10:
            
            if int(pos[0]) == 102 and int(pos[1]) == 125 and int(pos[2]) == -32:
                last_pos = pos
                continue
            
            
            print(f"activated by movement | distance : {distance_between_points(last_pos, pos)}")
            
            
            check = True
            focus_minecraft()
            
            sleep(1)
            
            pyautogui.press("F7")
            
            play_mp3(os.path.join(sys.path[0], "assets/alarm.mp3"))

        
        # if abs(last_yaw - yaw) > 90:
        #     print("activated by rotation")
        #     check = True
            
        #     sleep(1)
            
        #     pyautogui.press("F7")
            
        #     play_mp3(os.path.join(sys.path[0], "assets/alarm.mp3"))

        
        if tool is None or tool.slot != last_tool.slot or tool.selected != last_tool.selected:
            print("activated by tool")
            check = True
            
            sleep(1)
            
            pyautogui.press("F7")
            
            play_mp3(os.path.join(sys.path[0], "assets/alarm.mp3"))

        
        
        
        
        
        last_pos = player_position()
        last_yaw = yaw
        last_pitch = pitch
        
            
            
        sleep(.01)
        



if __name__ == "__main__":
    print("AVAST running")
    stop_event = threading.Event()
    reset_sound = [False]

    t1 = threading.Thread(target=kill_process, args=(stop_event, reset_sound,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event, reset_sound,), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
