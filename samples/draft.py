import threading
from queue import Queue
import copy
import time

start_time = time.time()
time.sleep(1)
end_time = time.time()

total_time = int(end_time) - int(start_time) + 12

print(total_time)