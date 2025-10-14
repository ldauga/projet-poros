import os, sys, io
import warnings

# Fix missing environment vars for Minescript
os.environ.setdefault("PATH", "")
os.environ.setdefault("SDL_AUDIODRIVER", "directsound")

# --- Temporarily silence only pygame's import noise ---
warnings.filterwarnings("ignore", module="pkg_resources")

_stdout = sys.stdout
_stderr = sys.stderr
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
try:
    import pygame
finally:
    sys.stdout = _stdout
    sys.stderr = _stderr
# --- End of silence block ---

def play_mp3(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
