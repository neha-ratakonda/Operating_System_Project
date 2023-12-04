import threading

max_passengers = 5
mutex = threading.Semaphore(1)#used to control access to the shared variable `passengers_in_car`. It ensures that only one thread at a time can modify the value of `passengers_in_car`.
#onboard = threading.Semaphore(0)
full = threading.Semaphore(0)#This semaphore is used to make sure the roller coaster doesn't start moving until it is full [i.e., until the specified number of passengers(number of passengers==Capacity) have boarded].

#boarding = threading.Semaphore(1) 

passengers_in_car = 0

def passenger():
    global passengers_in_car
    
    while True:
        
        mutex.acquire()#called before entering the critical section where `passengers_in_car` is modified
        #boarding.acquire()#when passenger empty has empty seats left, then only passenger can get it

#something we’re still working on
        
        passengers_in_car += 1
        print(f"Roller coaster is moving with {passengers_in_car} passengers")
        
        mutex.release()#called afterward to release the lock
        
        if onBoard == CAPACITY:
            full.release() #When a passenger thread increments `passengers_in_car` to the desired capacity , it releases the `full` semaphore
            
#         else:
#             boarding.release()
# WORK IN PROGRESS
#We encountered difficulties with the ‘boarding’ semaphore 
#We have a lot of ideas as to what semaphores to use to find the solution.
#If possible we will also try to expand our problem statement from a single roller coaster car to ‘n’ cars in the future.

            
def rollercoaster():
    
    global passengers_in_car
    
    while True:
        
        full.aquire() #This allows the `rollercoaster` function to proceed, indicating that the roller coaster is full and can start moving.
        
        print("The roller coaster is moving wohoooo !!!!")
        
