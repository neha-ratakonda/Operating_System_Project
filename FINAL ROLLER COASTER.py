# This is the final code of the Solution we came up with 

# Importing necessary  libraries
import threading  
import time
import random

CAPACITY = 6  # Passengers (because we are six passengers)
MAXRIDES = 3  # The maximum numbers of rides that our roller coaster rides 

# Initially setting both passengers and current number of rides
passengers_in_car = 0
current_rides = 0

# Create a semaphore named 'counter' with an initial value of 1 (We changed the name from mutex to counter for ease of use)
counter = threading.Semaphore(1)
# Create a semaphore named 'full' with an initial value of 0
full = threading.Semaphore(0)
# Create a semaphore named 'deboarding' with an initial value of 0
deboarding = threading.Semaphore(0)
# Create a semaphore named 'moving' with an initial value of 1
moving = threading.Semaphore(1)

# This is the main roller coaster function
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

# This is the function for passenger 
def passenger():
    global passengers_in_car

    while current_rides < MAXRIDES:
        # Arrive at the ride, wait for the roller coaster car
        if passengers_in_car < CAPACITY:
            moving.acquire() # When the roller coaster is moving the passenger can't move, hence the passnger has to wait until the roller coaster is stationary
       
        counter.acquire() # Shared variable counter for counting the passengers on board
        passengers_in_car += 1  # Boarding the car
        print("Passenger boarded !! Passengers on board: {}".format(passengers_in_car))

        if passengers_in_car == CAPACITY:
            full.release()

        counter.release()
        moving.release()
        
        #ride is happening in this duration

        deboarding.acquire()
        counter.acquire()

        passengers_in_car -= 1  # Deboarding the car
        print("Passenger left. Passengers on board: {}".format(passengers_in_car))

        if passengers_in_car > 0:
            deboarding.release()

        counter.release()

        # Enjoying the amusement park (Essentially waiting time)
        time.sleep(get_random_time())
        #We did this to try and simualate a real life amusement park where people roam around the park before getting back into a queue to wait for the ride 

def get_random_time():
    return random.uniform(1, 4)

roller_coaster_thread = threading.Thread(target=roller_coaster)
roller_coaster_thread.start() #The roller coaster arrives first

# Creating threads for each passenger
passenger_threads = []

for i in range(CAPACITY):
    passenger_thread = threading.Thread(target=passenger)
    passenger_thread.start()
    passenger_threads.append(passenger_thread)
    
# Waiting for the roller coaster thread to finish
roller_coaster_thread.join()

# Waiting for all passenger threads to finish
for thread in passenger_threads:
    thread.join()
