import pymem
import win32api
import time
from pymem.process import *

# offsets
LOCAL_PLAYER = 14592396
FORCE_JUMP = 86752472
HEALTH = 256
FLAGS = 260

def bhop() -> None:
    pm = pymem.Pymem('csgo.exe')

    client = module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    # hack loop
    while True:
        time.sleep(0.01)

        # if you press/hold the "space" key
        if not win32api.GetAsyncKeyState(0x20):
            continue
        
        local_player = int(pm.read_uint(client + LOCAL_PLAYER))
        # if player is available
        if not local_player:
            continue
        
        # if alive
        if not pm.read_uint(local_player + HEALTH):
            continue

        # if on the ground
        if pm.read_uint(local_player + FLAGS) & 1 << 0:
            # jump
            pm.write_uint(client + FORCE_JUMP, 6)
            time.sleep(.01)
            pm.write_uint(client + FORCE_JUMP, 4)
        
if __name__ == "__main__":
    bhop()
