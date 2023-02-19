# # # A list is an ordered collection of items, which can be of any type, such as numbers, strings, or other objects. Lists are mutable, which means that their items can be added, removed, or changed.
# #
# # # A dictionary is an unordered collection of key-value pairs, where each key is associated with a corresponding value. Keys are unique and immutable, while values can be of any type. Dictionaries are also mutable and can be changed by adding, removing, or changing key-value pairs.
# # # my_list = []
# # # for i in range(5, 56):
# # #     my_list.append(i)
# # # print(my_list)
# # #
# # # my_dict = {'apple': 2, 'banana': 3, 'orange': 5, 'grape': 1, 'kiwi': 4}
# # # print(my_dict)
# # #
# # # my_list_of_numbers = [1, 2, 3, 4, 5]
# # # updated_list = []
# # #
# # # for i in my_list_of_numbers:
# # #     updated_list.append(3 + i)
# # #
# # #
# # # print(updated_list)
# #
# # #
# # # data = [15, 9, 4, 21, 14, 18, 27, 31, 35, 40]
# # # new_data = []
# # #
# # # for num in data:
# # #     if num % 3 == 0 or num % 7 == 0:
# # #         new_data.append(num)
# # #
# # # print(new_data)
# #
# # myDict = {90: "A", 80: "B", 70: "C", 60: "D"}
# #
# # # Print the keys
# # print("Keys:")
# # for key in myDict:
# #     print(key)
# #
# # # Print the values
# # print("\nValues:")
# # for value in myDict.values():
# #     print(value)
# #
# # # Print the key-value pairs
# # print("\nKey-value pairs:")
# # for key, value in myDict.items():
# #     print(key, ":", value)
# #
# # # Print the key-value pairs in ascending order based on key
# # print("\nKey-value pairs in ascending order based on key:")
# # for key, value in sorted(myDict.items()):
# #     print(key, ":", value)
# #
# # # Print the key-value pairs in ascending order based on value
# # print("\nKey-value pairs in ascending order based on value:")
# # for key, value in sorted(myDict.items(), key=lambda item: item[1]):
# #     print(key, ":", value)
# #
# #
# # {'January': 31, 'February': 28, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31, 'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}
# # Instantiate the Truck properties.
# truck1 = Truck(env, "Ford", "X-102", 2010, 72800, "2000HP")
# print(f"Name: {truck1.name} \nModel: {truck1.model}.\n")
# '''*****************************************'''
# # Instantiate the SemiTruck properties.
# semi_truck = SemiTruck(env, "Volvo", "VNL", 2020, 10000, "800HP", 5000, 10, 2.8,3.2,5)
# print(f"Name: {semi_truck.name}, Model: {semi_truck.model}")
# # Call the attach_trailer function on the SemiTruck instance.
# semi_truck.attach_trailer()
# # call the size_dimension function of Truck class by SemiTruck subclass.
# l = semi_truck.length
# b = semi_truck.width
# h = semi_truck.height
# print(f"Size of a Semi-Truck: {semi_truck.size_dimension_(l,b,h):.2f}.")
# x = semi_truck.trailer_capacity(25000)
# print(f"The capacity of a trailer: {x:.2f} lbs.\n")
#
# '''*******************************************'''
#
# # Instantiate Box Truck properties.
# box_truck = BoxTruck(env, "Ford", "FX-350",2018,48876,"375HP",5.5,2.5,2.2,6.6)
# print(box_truck.name)
# item1 = box_truck.add_list("box1")
# item2 = box_truck.add_list("box2")
# item3 = box_truck.add_list("box3")
# item4 = box_truck.add_list("box4")
# item5 = box_truck.add_list("box5")
# print(box_truck.cargo_list)
#
# '''********************************************'''
#
# deck_truck = DeckTruck(env, "Xplore","Mx-13",2010,55892,"325HP",8, "55000lbs")
# x = deck_truck.stop_truck()
# print(x)
# y = deck_truck.ramp_access(6)
# print(y)

import simpy

class Truck:
    def __init__(self, name, env, speed):
        self.name = name
        self.env = env
        self.speed = speed

    def drive(self, route):
        for i in range(len(route)-1):
            src, dst = route[i], route[i+1]
            distance = dst[0] - src[0]
            travel_time = distance / self.speed
            print(f"{self.name} is driving from {src[1]} to {dst[1]} for {travel_time:.2f} time units")
            yield self.env.timeout(travel_time)
            if dst[2]: # if destination has a red light
                print(f"{self.name} is waiting at {dst[1]} for green light at time {self.env.now}")
                yield dst[2] # wait for green light
        print(f"{self.name} has arrived at {dst[1]} at time {self.env.now}")

env = simpy.Environment()
truck1 = Truck('Truck 1', env, 50)
route1 = [((0, 0), 'Point A'), ((100, 0), 'Point B', env.event())]
env.process(truck1.drive(route1))

truck2 = Truck('Truck 2', env, 60)
route2 = [((0, 0), 'Point C'), ((100, 0), 'Point D', env.event())]
env.process(truck2.drive(route2))

env.run(until=50)
