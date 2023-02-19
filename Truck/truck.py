import simpy
import random
import geopy.distance

class Truck:
    def __init__(self,env, name, model, year, mileage, engine):
        self.env = env
        self.name = name
        self.model = model
        self.year = year
        self.mileage = mileage
        self.engine = engine
        self.gas_type = None
        self.gas_range = None

    def queue_up(self, endpoint): #
        x = random.randint(1, 10) # truck queuing at different time units.
        yield self.env.timeout(x)
        arrival_time = self.env.now
        print(f"{self.name} is queueing up at {endpoint} at {arrival_time} time units.")

        entry_time = 4 + x # 4 time units is a time needed to enter a road/highway after queue time.
        print(f"{self.name} is entering a road/highway from {endpoint} at {entry_time} time units.\n")

    def drive(self, route, speed):  # route is a tuple that has longitude, latitude, and start and end location.
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            distance = geopy.distance.geodesic(start[0], end[0]).km
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
                    print(
                        f"{self.name} is proceeding cautiously at intersection for yellow light at time {time_yellow} seconds.")
                    yield self.env.event()  # wait for green light

                else:
                    print(
                        f"{self.name} has crossed intersection.")  # the road segment length implementation is still confusing. No, implementation of time calculation.

            print(f"{self.name} has reached destination {end[1]} at time {time_required:.5f} seconds.")

    def mileage_(self, miles):
        self.mileage += miles
        return self.mileage

    def size_dimension_(self, l, b, h):
        self.size_dimension = l * b * h
        return self.size_dimension

    def gas_efficiency(self, mph, amount):
        self.gas_range = mph * amount
        return self.gas_range

    def stop_truck(self):
        return "Stop the truck."


class SemiTruck(Truck):
    def __init__(self, env, name, model, year, mileage, engine, weight, length, width, height,axles):
        super().__init__(env, name, model, year, mileage, engine)
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight  # total weight of a trailer
        self.axles = axles

    def attach_trailer(self):
        print(f"Attached trailer length is {self.length} m, width is {self.width} m, height is {self.height} m, and weight is {self.weight} lbs.")

    def detach_trailer(self):
        print(f"Trailer of weight {self.weight} is detached.")

    def trailer_capacity(self,weight_capacity):
        factor = 0
        capacity = 0
        if self.axles == 2:
            factor = 2.5
        elif self.axles == 3:
            factor = 3.5
        elif self.axles == 5:
            factor = 5.5
        else:
            factor = 4.0

        capacity = weight_capacity * factor
        return capacity

class BoxTruck(Truck):
    def __init__(self, env, name, model, year, mileage, engine, length, width, height,load_capacity):
        super().__init__(env, name, model, year, mileage, engine)
        self.length = length
        self.width = width
        self.height = height
        self.truck_space = None
        self.load_capacity = load_capacity # load capacity per volume: in ton.
        self.cargo_list = []

    def cargo_space(self):
        self.truck_space = self.length * self.width * self.height
        return self.truck_space

    # allows the labor to keep the track of the cargo inventory in the box truck.
    def add_list(self, item):
        self.cargo_list.append(item)

    def box_capacity(self):
        self.load_capacity = self.length * self.width * self.height * self.load_capacity
        return self.load_capacity


class DeckTruck(Truck):
    def __init__(self, env, name, model, year, mileage, engine, length,load_capacity):
        super().__init__(env, name, model, year, mileage, engine)
        self.length = length # length of a truck.
        self.ramp_length = 0  # length of a ramp.
        self.load_capacity = load_capacity


    def ramp_access(self,length):
        if length < self.length:
            self.ramp_length = length
            return "Ramp Extended."
        else:
            return "Ramp is longer than the truck itself."


# create the simulation environment
env = simpy.Environment()

'''**************** Semi Truck Instantiation ************************'''
semi_truck1 = SemiTruck(env,"Semi Truck 1", "Model 1", 2012,58000,"500hp", 5, 2.5, 2.3, 5000, 4)
print(f"Name: {semi_truck1.name}, Model: {semi_truck1.model}")
# Call the attach_trailer function on the SemiTruck instance.
semi_truck1.attach_trailer()
# call the size_dimension function of Truck class by SemiTruck subclass.
l = semi_truck1.length
b = semi_truck1.width
h = semi_truck1.height
print(f"Size of a Semi-Truck: {semi_truck1.size_dimension_(l,b,h):.2f}.")
x = semi_truck1.trailer_capacity(25000)
print(f"The capacity of a trailer: {x:.2f} lbs.\n")

end_point = ["Point A", "Point B", "Point C", "Point D", "Point E"] # name of end points of a map.
env.process(semi_truck1.queue_up(end_point[random.randint(0,len(end_point) - 1)]))


semi_truck2 = SemiTruck(env,"Semi Truck 2", "Model 2", 2015,40020,"475hp", 5, 2.5, 2.3, 8000, 4)
print(f"Model: {semi_truck2.model}, Engine: {semi_truck2.engine}")
env.process(semi_truck2.queue_up(end_point[random.randint(0,len(end_point) - 1)]))

semi_truck3 = SemiTruck(env,"Semi Truck 3", "Model 3", 2018,35180,"550hp", 5, 2.5, 2.3, 8000, 5)
print(f"Year: {semi_truck3.year}, Axles: {semi_truck3.axles}\n")
env.process(semi_truck3.queue_up(end_point[random.randint(0,len(end_point) - 1)]))


'''**************** Box Truck Instantiation ************************'''
box_truck1 = BoxTruck(env, "Ford", "FX-350",2018,48876,"375HP",5.5,2.5,2.2,6.6)
print(box_truck1.name)
item1 = box_truck1.add_list("box1")
item2 = box_truck1.add_list("box2")
item3 = box_truck1.add_list("box3")
item4 = box_truck1.add_list("box4")
item5 = box_truck1.add_list("box5")
print(box_truck1.cargo_list)

box_truck2 = BoxTruck(env, "Volks", "VS-310",2015,40976,"425HP",5.2,2.9,2.4,6.6)
print(box_truck2.box_capacity())
env.process(box_truck1.queue_up(end_point[random.randint(0,len(end_point) - 1)]))
env.process(box_truck2.queue_up(end_point[random.randint(0,len(end_point) - 1)]))

'''**************** Deck Truck Instantiation ************************'''
deck_truck1 = DeckTruck(env, "Xplore","Mx-13",2010,55892,"325HP",8, "55000lbs")
x = deck_truck1.stop_truck()
print(x)
y = deck_truck1.ramp_access(6)
print(y)

deck_truck2 = DeckTruck(env, "Deck Truck 2","Mx-16",2012,50892,"375HP",7, "55000lbs")
deck_truck3 = DeckTruck(env, "Deck Truck 3","MB-15",2016,50332,"325HP",9, "59000lbs")

env.process(deck_truck2.queue_up(end_point[random.randint(0,len(end_point) - 1)]))
env.process(deck_truck3.queue_up(end_point[random.randint(0,len(end_point) - 1)]))

"""Intersection Simulation- From Point A to Point B"""
route1 = [((52.22, 21.01), "Point A"), ((53.1, 16.9), "Point B", "intersection")]
route2 = [((42.22, 24.01), "Point C"), ((43.1, 19.9), "Point D", "intersection")]
env.process(semi_truck1.drive(route1, 50))
env.process(box_truck2.drive(route2, 50))

env.run(until=50)

