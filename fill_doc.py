import subprocess, os, sys, time

# Start LibreOffice in listening mode
profile_dir = "/tmp/lo_profile_lab1"
os.makedirs(profile_dir, exist_ok=True)

# Kill any existing soffice
subprocess.run(["pkill", "-f", "soffice"], capture_output=True)
time.sleep(1)

# Start LibreOffice listener
lo_proc = subprocess.Popen([
    "soffice", "--headless", "--invisible",
    f"-env:UserInstallation=file://{profile_dir}",
    "--accept=socket,host=localhost,port=2002;urp;"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("LO started, pid:", lo_proc.pid)
time.sleep(3)

# Connect via UNO
import uno
from com.sun.star.beans import PropertyValue

local_ctx = uno.getComponentContext()
resolver = local_ctx.ServiceManager.createInstanceWithContext(
    "com.sun.star.connection.UriResolver", local_ctx
)

try:
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
    )
    print("Connected to LO")
except Exception as e:
    print("Connection failed:", repr(e))
    # Try direct desktop
    smgr = local_ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", local_ctx)
    print("Desktop created directly")

# Convert screenshots to base64 and insert
import base64
screenshots = {
    "task1": "/tmp/task_node_versions.png",
    "task4": "/tmp/task_website.png",
    "task5": "/tmp/task_website.png",  # reuse
    "task6": "/tmp/task_website.png",  # reuse
}

for k, v in screenshots.items():
    if os.path.exists(v):
        print(f"  {k}: {v} exists, size={os.path.getsize(v)}")
    else:
        print(f"  {k}: MISSING")

lo_proc.terminate()
