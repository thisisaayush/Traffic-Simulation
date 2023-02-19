import simpy

class Truck:
    def __init__(self, name, env):
        self.name = name
        self.env = env

    def drive(self, route, speed):
        for i in range(len(route)-1):
            src, dst = route[i], route[i+1]
            distance = dst[0][0] - src[0][0]
            travel_time = distance / speed
            print(f"{self.name} is driving from {src[1]} to {dst[1]} for {travel_time:.2f} time units")
            yield self.env.timeout(travel_time)
            if dst[2]: # if destination has a red light
                print(f"{self.name} is waiting at {dst[1]} for green light at time {self.env.now}")
                yield dst[2] # wait for green light
        print(f"{self.name} has arrived at {dst[1]} at time {self.env.now}")

env = simpy.Environment()
truck1 = Truck('Truck 1', env)
route1 = [((0, 0), 'Point A'), ((100, 0), 'Point B', env.event())]
env.process(truck1.drive(route1,50))

truck2 = Truck('Truck 2', env)
route2 = [((0, 0), 'Point C'), ((100, 0), 'Point D', env.event())]
env.process(truck2.drive(route2,60))

env.run(until=50)
