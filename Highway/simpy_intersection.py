import simpy
import random
# 5 trucks simulation trying to pass through an intersection from 4 different directions.
def truck(env, name, direction, intersection):

    arrival_time = env.now # monitors arrival time of a truck.
    print(f"Truck {name} from {direction} arrived at {arrival_time} time.")
    with intersection.request() as req: # truck requesting access to intersection.
        yield req # waits until the intersection is available.
        # the wait_time will monitor the random wait time between 5 and 15 sec before it can pass intersection.
        wait_time = random.uniform(5, 15)
        yield env.timeout(wait_time) # wait random amount of time.

        departure_time = env.now
        print(f"Truck {name} from {direction} departed at {departure_time:.2f} time.")

# create the simulation environment
env = simpy.Environment()
# create the intersection resource with a capacity of 1.
intersection = simpy.Resource(env, capacity=1)

direction_list = ['East','West','North','South']
for i in range(1,6):
    env.process(truck(env, i, direction_list[random.randint(0,len(direction_list) - 1)], intersection))

# run the simulation for 500 time units.
env.run(until=500)
