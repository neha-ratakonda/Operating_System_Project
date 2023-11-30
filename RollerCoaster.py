import threading
import time
import random

CAPACITY = 3  # Capacity of the roller coaster car

onBoard = 0  # Number of passengers currently on board
mutex = threading.Semaphore(1)  # Semaphore for controlling access to shared variables
boarding = threading.Semaphore(0)  # Semaphore for signaling that a passenger is ready to board
full = threading.Semaphore(0)  # Semaphore for signaling that the roller coaster is full and ready to move
empty = threading.Semaphore(0)  # Semaphore for signaling that all passengers have left the roller coaster
leave = threading.Semaphore(0)  # Semaphore for signaling that a passenger has left the roller coaster

def init_sems():
    pass  # Initialization function, currently empty

def roller_coaster():
    global onBoard

    while True:
        boarding.release()  # Signal that the roller coaster is ready for boarding
        full.acquire()      # Wait until the roller coaster is full

        # Time for the ride
        print("Roller coaster is moving with {} passengers".format(onBoard))

        leave.release()  # Signal that passengers can start leaving
        empty.acquire()  # Wait until all passengers have left

def passenger():
    global onBoard

    while True:
        # Arrive at the ride, wait for the roller coaster car
        boarding.acquire()
        mutex.acquire()

        onBoard += 1  # Board the car
        print("Passenger boarded. Passengers on board: {}".format(onBoard))

        if onBoard == CAPACITY:
            full.release()  # Signal that the roller coaster is full
        else:
            boarding.release()  # Allow the next passenger to board

        mutex.release()

        # Enjoy the ride
        print("Yahoooooo, this ride is cool")

        leave.acquire()  # Wait for permission to leave
        mutex.acquire()

        onBoard -= 1  # Leave the car
        print("Passenger left. Passengers on board: {}".format(onBoard))

        if onBoard > 0:
            leave.release()  # Signal that another passenger can leave
        else:
            empty.release()  # Signal that all passengers have left

        mutex.release()

        # Enjoy the amusement park
        time.sleep(get_random_time())

def get_random_time():
    return random.uniform(1, 3)  # Returns a random time between 1 and 3 seconds

if __name__ == "__main__":
    roller_coaster_thread = threading.Thread(target=roller_coaster)
    passenger_threads = []

    for i in range(CAPACITY):
        passenger_thread = threading.Thread(target=passenger)
        passenger_threads.append(passenger_thread)

    roller_coaster_thread.start()  # Start the roller coaster thread

    for thread in passenger_threads:
        thread.start()  # Start each passenger thread

    roller_coaster_thread.join()  # Wait for the roller coaster thread to finish

    for thread in passenger_threads:
        thread.join()  # Wait for each passenger thread to finish

