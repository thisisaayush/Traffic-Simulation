import simpy
import geopy.distance
class Truck:
    def __init__(self, env, name):
        self.env = env
        self.name = name

    def drive(self, route, speed): # route is a tuple that has longitude, latitude, and start and end location.
        for i in range(len(route)-1):
            start, end = route[i], route[i+1]
            distance = geopy.distance.geodesic(start[0],end[0]).km
            time_required = distance / speed

            if "intersection" in end:
                signal = input("Enter the light: ")
                if signal == "red":
                    stop_time = 0.005
                    time_required += stop_time
                    yield self.env.timeout(stop_time)
                    time_red = env.now
                    print(f"{self.name} is waiting at intersection for green light at time {time_red} seconds.")

                elif signal == "yellow":
                    proceed_time = 0.0025
                    time_required += proceed_time
                    yield self.env.timeout(proceed_time)
                    time_yellow = env.now
                    print(f"{self.name} is proceeding cautiously at intersection for yellow light at time {time_yellow} seconds.")

                else:
                    print(f"{self.name} has crossed intersection.") # the road segment length implementation is still confusing. No, implementation of time calculation.

            print(f"{self.name} has reached destination {end[1]} at time {time_required:.5f} seconds.")

env = simpy.Environment()

box_truck2 = Truck(env, "Volks")
truck1 = Truck(env, "Truck 1")
route1 = [((59.22, 21.01), "Point A"), ((63.1, 23.9), "Point B", "intersection")]
route2 = [((41.12, 24.01), "Point C"), ((43.11, 19.8), "Point D", "intersection")]
env.process(truck1.drive(route1, 50))
env.process(box_truck2.drive(route2, 50))
env.run(until=50)

