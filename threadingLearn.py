import time 
import threading

counter = 0

def hello():
    global counter
    while True:
        print("hello")
        time.sleep(5)
        counter +=1

def print_counter():
    global counter
    while True:
        print(counter)
        time.sleep(10)

thread_printHello = threading.Thread(target=hello)
thread_printcounter = threading.Thread(target=print_counter)
thread_printHello.daemon = True
thread_printcounter.daemon = True

thread_printHello.start()
thread_printcounter.start()

for i in range(10):
    time.sleep(3)
    print("i am in main")
