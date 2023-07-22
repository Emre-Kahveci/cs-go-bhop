import pymem
import win32api
import time
from pymem.process import *

# offsets
LOCAL_PLAYER = 0x00DEA98C
FORCE_JUMP = 0x52BBCD8
HEALTH = 0x100
FLAGS = 0x104

def bhop() -> None:
    pm = pymem.Pymem('csgo.exe') # find the exe file
    client = module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll

    # hack loop
    while True:
        time.sleep(0.01)

        # if you press/hold the "space" key
        if not win32api.GetAsyncKeyState(0x20):
            continue
        
        # if player is available
        local_player = pm.read_int(client + LOCAL_PLAYER)
        if not local_player:
            continue
        
        # if alive
        if not pm.read_int(local_player + HEALTH):
            continue

        # if on the ground
        if pm.read_int(local_player + FLAGS) & 1 << 0:
            # jump
            pm.write_int(client + FORCE_JUMP, 6)
            time.sleep(.01)
            pm.write_int(client + FORCE_JUMP, 4)
        
if __name__ == "__main__":
    bhop()
