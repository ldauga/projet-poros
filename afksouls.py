from time import sleep
from pyautogui import click, moveTo

from system.lib.minescript import execute


for _ in range(20):
    execute("afk")
    sleep(0.2)
    moveTo(1129, 380)
    sleep(0.2)
    click()
    moveTo(851, 379)
    sleep(0.2)
    click()
