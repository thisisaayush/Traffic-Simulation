class Road:
    def __init__(self, name, nodes, segment_length, initial_position, curr_position, sign_board):
        self._name = name
        self.nodes = nodes
        self.segment_length = segment_length
        self.initial_position = initial_position
        self.current_position = curr_position
        self.sign_board = sign_board
        self.conflict = False

    def count_intersections(self, point_A, point_B):
        start = self.nodes.index(point_A)
        end = self.nodes.index(point_B)
        return abs(end - start) - 1

    def road_intersection(self):
        if self.sign_board.lower() == "yield":
            self.conflict = input("Is there a conflict? True/False:")
            if self.conflict == True:
                return "Stop."
            return "Yield Sign: Slow down your vehicle.."

        elif self.sign_board.lower() == "stop":
            return "Stop Sign: Stop your vehicle."

        elif self.sign_board.lower() == "traffic light":
            self.traffic_light = input("Enter light signal:")
            if self.traffic_light.lower() == "red":
                return "Stop."
            elif self.traffic_light.lower() == "yellow":
                return "Prepare to stop."
            elif self.traffic_light.lower() == "green":
                if self.conflict == True:
                    return "Stop."
                return "Proceed cautiously."

    def approaching_intersection(self):
        if self.segment_length <= self.initial_position + self.current_position:
            return self.road_intersection()
        else:
            return "No intersection is approaching."

class Highway:
    def __init__(self, name, nodes, segment_length, initial_position, curr_position, traffic_light):
        self.name = name
        self.nodes = nodes # list of intersections.
        self.segment_length = segment_length
        self.initial_position = initial_position
        self.curr_position = curr_position
        self.traffic_light = traffic_light

    def ramp_intersection(self, name, point):
        if name.lower() == "on ramp": # road to highway.
            if point in self.nodes:
                return "Enter at or near the speed of highway vehicles."

            return "No on-ramp exist."

        elif name.lower() == "off ramp": # highway to road.
            if point in self.nodes:
                return "Exit at or near the speed of road vehicles."
            return "No off-ramp exist."

    def highway_intersection(self, other_highway):
        if set(self.nodes).intersection(other_highway.nodes):
            return set(self.nodes).intersection(other_highway.nodes)
        return "No Intersections."

    def traffic_light(self):
        if self.traffic_light.lower() == "red":
            return "Stop."
        elif self.traffic_light.lower() == "yellow":
            return "Prepare to stop."
        elif self.traffic_light.lower() == "green":
            return "Proceed cautiously."

    def approaching_intersection(self):
        if self.segment_length <= self.initial_position + self.current_position:
            return "Highway Intersection ahead."
        else:
            return "No intersection is approaching."



highway1 = Highway("Highway1", ["int1", "int2","int3", "int4"], 1000, 100, 500, "green")
highway2 = Highway("Highway2", ["int4", "int5","int6", "int7"], 1500, 200, 900, "yellow")
highway_intersections = highway1.highway_intersection(highway2)
ramp_test = highway1.ramp_intersection("off ramp","int4")
print(ramp_test)
print("The two highway intersect at ", highway_intersections, ".")


road1 = Road("Road1",["1","2","3","4","5"], 15,10,8, "yield")
print(road1.approaching_intersection())
print("Count intersections: ", road1.count_intersections("1","5"))