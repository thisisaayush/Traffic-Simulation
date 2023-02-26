import simpy
import random
import geopy.distance

class Truck:
    def __init__(self, env, name, model, speed):
        self.env = env
        self.name = name
        self.model = model
        self.speed = speed
        self.current_position = None

    def vehicle_size(self, l,b,h):
        return l * b * h

    # calculate the total distance base on intersection.
    def total_distance(self, road_segments): # road segments is a parameter that consists of list of tuples.
        sum_distance = 0
        start_position = 0
        end_position = 0

        for i, segment in enumerate(road_segments):
            if i == 0:
                start_position = segment[0]
            else:
                start_position = end_position

            end_position = segment[1]
            distance = geopy.distance.distance(start_position, end_position)
            sum_distance += distance.km

        return sum_distance
    def truck_queue(self, endpoint, queue): # queues truck at the endpoints A, B, C, D, E.
        x = random.randint(1, 10) # truck queuing at different time units.
        yield self.env.timeout(x)
        arrival_time = self.env.now
        print(f"{self.name} is queueing up at {endpoint} at {arrival_time} time units.")
        queue.append(self)
        entry_time = 4 + arrival_time # 4 time units is a time needed to enter a road/highway after queue time.
        print(f"{self.name} is entering a road/highway from {endpoint} at {entry_time} time units.\n")
        queue.pop(0)

    # road_segments: has the co-ordinates of road segments in list-tuple format.
    def move_truck(self, env, road_segments, intersections_point): #move along-ness from point 1 to point 2.
        travel_time = 0
        for segment in road_segments:
            start_position = segment[0]
            end_position = segment[1]

            distance = geopy.distance.distance(start_position, end_position).km
            travel_time += distance / self.speed

            yield env.timeout(travel_time)

            if end_position in intersections_point: # traffic signal.
                wait_time = 00.5 # constant wait time at intersection despite lights color.
                travel_time += wait_time
                yield env.timeout(wait_time)

            if road_segments[-1] == (start_position,end_position):
                return("Reached Destination. Time Required: {}.".format(travel_time))
class SemiTruck(Truck):
    def __init__(self, env, name, model, speed, axles, num_dirvers, trailer_attached=False, trailer_detached = False):
        super().__init__(env, name, model, speed)
        self.axles = axles
        self.drivers = num_dirvers
        self.trailer_attached = trailer_attached
        self.trailer_detached = trailer_detached

    def trailer_attached_(self):
        if self.trailer_attached == True:
            return "Trailer Attached."

    def trailer_detached_(self):
        if self.trailer_detached == True:
            return "Trailer Detached."

    def trailer_capacity(self,capacity):
        factor = 0 # factor will allow to estimate the total weight a truck can carry.
        weight_capacity = 0
        if self.axles == 2:
            factor = 2.5
        elif self.axles == 3:
            factor = 3.5
        elif self.axles == 5:
            factor = 5.5
        else:
            factor = 4.0

        weight_capacity = capacity * factor
        return weight_capacity

class BoxTruck(Truck):
    def __init__(self, env, name, model, speed, load_per_volume):
        super().__init__(env, name, model, speed)
        self.load = load_per_volume
        self.cargo_list = []

    # allows the labor to keep the track of the cargo inventory in the box truck.
    def add_list(self, item):
        self.cargo_list.append(item)

    def box_capacity(self, l, b, h):
        return l * b * h * self.load

class DeckTruck(Truck):
    def __init__(self, env, name, model, speed, length, breadth, ramp_length):
        super().__init__(env, name, model, speed)
        self.deck_area = length * breadth
        self.ramp_length = ramp_length

    def ramp_access(self,length):
        if length <= self.ramp_length:
            self.ramp_length = length
            return " ramp is extendable."
        else:
            return " ramp is not extendable. Ramp length is longer than the deck it self.."

# create the simulation environment
env = simpy.Environment()
"""                   Semi Truck                """
semitruck1 = SemiTruck(env, "Semi Truck 1", "Semi Model 1", 55, 3, 2, True, False)
print(semitruck1.vehicle_size(15,5,6))
print(semitruck1.trailer_attached_())

semitruck2 = SemiTruck(env, "Semi Truck 2", "Semi Model 2", 60, 4, 2, False, True)
print(semitruck2.trailer_detached_())
print(semitruck2.trailer_capacity(25000))
print()
"""                   Box Truck                 """
boxtruck1 = BoxTruck(env, "Box Truck 1", " Box Model 1", 58, 200)
print("Box Truck 1 load capacity: ", boxtruck1.load)
print(f"{boxtruck1.name} model is  {boxtruck1.model}.")

boxtruck2 = BoxTruck(env, "Box Truck 2", " Box Model 2", 65, 175)
print("Box Truck Size: ",boxtruck2.vehicle_size(7,3,2.4), "meter cube.")

print()
"""                   Deck Truck                """
decktruck1 = DeckTruck(env, "Deck Truck 1", "Deck Model 1", 54, 5, 2.5, 1.25)
print(f"{decktruck1.name} model is {decktruck1.model}.")
decktruck2 = DeckTruck(env, "Deck Truck 2", "Deck Model 2", 50, 5.2, 2.2, 1.2)
print(f"{decktruck2.name} {decktruck2.ramp_access(1.0)}")

"""                    End Points               """
endpoints = {"Point A" : [], "Point B":[], "Point C":[], "Point D":[], "Point E":[]} #the endpoint will queue list of truck at the endpoint declared in there.

print("\nThe Simulation of Endpoint Truck Queuing.\n")
def generate_truck(env, endpoint, queue):
    while True:
        yield env.timeout(10)
        truck = Truck(env, "Truck", "Model", 60)
        env.process(truck.truck_queue(endpoint, queue))

for endpoint in ["Point A", "Point B", "Point C", "Point D", "Point E"]:
    env.process(generate_truck(env, endpoint, endpoints[endpoint]))

env.run(until=25)

print()

road_segments = [ ((50.12,62.02),(50.15,62.04)),
                  ((50.15,62.04),(50.16,62.08)),
                  ((50.16,62.08),(50.21,62.14)),
                  ((50.21,62.14),(50.23,62.17)),
                  ((50.23,62.17),(50.55,62.35))
                  ]
intersections_point = [
                 ((50.15,62.04),(50.16,62.08)),
                 ((50.23,62.17),(50.55,62.35))
                ]

print(f"Total Distance: {decktruck2.total_distance(road_segments):.2f} km")
x = decktruck1.move_truck(env,road_segments,intersections_point)
print(x)