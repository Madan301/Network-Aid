import pyfiglet
import os
result = pyfiglet.figlet_format("Network-Aid")
print(result)
print("[*]Enter '1' for ddos detection mode")
print("[*]Enter '2' for network usage monitoring mode")
a = input("Enter mode: ")
if a == '1':
    print("[*]DDOS detection mode has been enabled")
    cmd = "python3 ddos.py"
    os.system(cmd)
elif a == '2':
    print("[*]Network usage tracking mode has been enabled")
    cmd = "python3 monitor.py"
    os.system(cmd)
                     
