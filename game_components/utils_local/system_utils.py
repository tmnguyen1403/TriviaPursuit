import platform

def is_mac():
    system = platform.system()
    return system == "Darwin"

def is_windows():
    system = platform.system()
    return system == "Windows"