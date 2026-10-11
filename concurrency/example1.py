import threading
import time

def worker():
    print("Worker started")
    time.sleep(1)
    print("Worker finished")

thread = threading.Thread(target=worker)
thread.start()

print("Main thread continues")

thread.join()
print("All done")