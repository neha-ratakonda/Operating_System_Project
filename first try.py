import threading

max_passengers = 5
mutex = threading.Semaphore(1)
#onboard = threading.Semaphore(0)
full = threading.Semaphore(0)
#boarding = threading.Semaphore(1) 

passengers_in_car = 0

def passenger():
    global passengers_in_car
    
    while True:
        
        mutex.acquire()
        #boarding.acquire()#when passenger empty has empty seats left, then only passenger can get it

#something we’re still working on
        
        passengers_in_car += 1
        print(f"Roller coaster is moving with {passengers_in_car} passengers")
        
        mutex.release()
        
        if onBoard == CAPACITY:
            full.release()
            
#         else:
#             boarding.release()
# WORK IN PROGRESS
            
def rollercoaster():
    
    global passengers_in_car
    
    while True:
        
        full.aquire()
        
        print("The roller coaster is moving wohoooo !!!!")
        
