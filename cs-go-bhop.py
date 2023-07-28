import pymem
import win32api
import time
from pymem.process import *

# offsets
localPlayer = 0x00DEA98C
forceJump = 0x52BBCD8
health = 0x100
flags = 0x104

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
        local_player = pm.read_int(client + localPlayer)
        if not local_player:
            continue
        
        # if alive
        if not pm.read_int(local_player + health):
            continue

        # if on the ground
        if pm.read_int(local_player + flags) & 1 << 0:
            # jump
            pm.write_int(client + forceJump, 6)
            time.sleep(.01)
            pm.write_int(client + forceJump, 4)
        
if __name__ == "__main__":
    bhop()
