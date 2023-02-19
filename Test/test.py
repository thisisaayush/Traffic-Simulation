import simpy
import random

class Truck:
    def __init__(self, name, env):
        self.env = env
        self.name = name

    def queue_up(self, endpoint):
        x = random.randint(1, 10) # truck queuing at different time units.
        yield self.env.timeout(x)
        arrival_time = self.env.now
        print(f"Truck {self.name} is queueing up at {endpoint} at {arrival_time} time units.")

        entry_time = 4 + x # 4 time units is a time needed to enter a road/highway after queue time.
        print(f"Truck {self.name} is entering a road/highway from {endpoint} at {entry_time} time units.\n")


env = simpy.Environment()

end_point = ["Point A", "Point B", "Point C", "Point D", "Point E"] # name of end points of a map.
for i in range(1,6):
    truck = Truck(f"{i}", env)
    env.process(truck.queue_up(end_point[random.randint(0,len(end_point) - 1)]))

env.run(until=25)