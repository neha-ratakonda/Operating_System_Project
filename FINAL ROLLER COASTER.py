import threading
import time
import random

CAPACITY = 6  # C passengers
MAXRIDES = 3


passengers_in_car = 0
current_rides = 0

counter = threading.Semaphore(1)
full = threading.Semaphore(0)
deboarding = threading.Semaphore(0)
moving = threading.Semaphore(1)

def roller_coaster():
    global passengers_in_car
    global current_rides

    while current_rides < MAXRIDES:
        
        full.acquire()      # Wait until full
        moving.acquire()    # Only when the coaster is full it'll start moving
        
        # Time for the ride
        print("Roller coaster is moving with {} passengers".format(passengers_in_car))

        moving.release() # Roller coaster will stop moving once the ride is finished
        deboarding.release()
        current_rides += 1

def passenger():
    global passengers_in_car

    while current_rides < MAXRIDES:
        # Arrive at the ride, wait for the roller coaster car
        if passengers_in_car < CAPACITY:
            moving.acquire() # When the roller coaster is moving the passenger can't move, hence the passnger has to wait until the roller coaster is stationary
       
        counter.acquire() # Shared variable counter for counting the passengers on board
        passengers_in_car += 1  # Board the car
        print("Passenger boarded. Passengers on board: {}".format(passengers_in_car))

        if passengers_in_car == CAPACITY:
            full.release()
            # gate()
        

        counter.release()
        moving.release()
        
        #ride is happening in this duration

        deboarding.acquire()
        counter.acquire()

        passengers_in_car -= 1  # deboarding the car
        print("Passenger left. Passengers on board: {}".format(passengers_in_car))

        if passengers_in_car > 0:
            deboarding.release()

        counter.release()

        # Enjoying the amusement park
        time.sleep(get_random_time())
        #We did this to try and simualate a real life amusement park where people roam around the park before getting back into a queue to wait for the ride 

def get_random_time():
    return random.uniform(1, 4)

roller_coaster_thread = threading.Thread(target=roller_coaster)
roller_coaster_thread.start() #The roller coaster arrives first

passenger_threads = []

for i in range(CAPACITY):
    passenger_thread = threading.Thread(target=passenger)
    passenger_thread.start()
    passenger_threads.append(passenger_thread)
    

roller_coaster_thread.join()

for thread in passenger_threads:
    thread.join()
