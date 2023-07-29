import pymem
import win32api
import time
import requests

def get_offset(url = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the JSON file: {e}")
        return None

def bhop(offsets = get_offset()) -> None:
    pm = pymem.Pymem('csgo.exe') # find the exe file
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll

    # hack loop
    while True:
        time.sleep(0.01)

        # if you press/hold the "space" key
        if not win32api.GetAsyncKeyState(0x20):
            continue
        
        # if player is available
        localPlayer = pm.read_int(client + offsets["signatures"]["dwLocalPlayer"])
        if not localPlayer:
            continue
        
        # if alive
        if not pm.read_int(localPlayer + offsets["netvars"]["m_iHealth"]):
            continue

        # if on the ground
        if pm.read_int(localPlayer + offsets["netvars"]["m_fFlags"]) & 1 << 0:
            # jump
            pm.write_int(client + offsets["signatures"]["dwForceJump"], 6)
            time.sleep(.01)
            pm.write_int(client + offsets["signatures"]["dwForceJump"], 4)
        
if __name__ == "__main__":
    bhop()
