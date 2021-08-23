from gen.mission_loader import MissionLoader
from gen.fault_specification import FaultSpecification
from gen.sim_interface import SimInterface
import random
from dsl.mission.Sensor import Sensor
from dsl.mission.Coordinates import Coordinates

class CI:
	
    total_goal_violations = [] 
    goal_violations_per_fault = {}
    time = 0
    
    def __init__(self):
        self.sim_interface = SimInterface()
        self.mission = MissionLoader().load_mission()
        self.sim_interface.start()
        

    def reset_system_state(self, fs):
        self.mission = MissionLoader().load_mission()
        self.fault_specification = fs
        self.sim_interface.mission = self.mission
        self.total_goal_violations = [0 for _ in range(self.mission.duration)]
        self.goal_violations_per_fault = {}
        self.time = 0

    def update_goal_violations(self, gid):
        self.total_goal_violations[self.time] += 1
        if gid in self.goal_violations_per_fault.keys():
            self.goal_violations_per_fault[gid] += 1
        else:
            self.goal_violations_per_fault[gid] = 1

    def update_system_state(self):
        """ Update mission state """
        for robot in self.mission.robots.values():
            robot.update_position(self.sim_interface.get_POSITION(robot))
            robot.update_energy(self.sim_interface.get_ENERGY(robot))
            robot.update_speed(self.sim_interface.get_SPEED(robot))
            for sc in robot.subcomponents.values():
                if isinstance(sc, Sensor) and sc.state == "Active":
                    sample = self.sim_interface.get_sensor_sample(sc)
                    sc.samples.append(sample)
            """print(robot.position.x)
            print(robot.position.y)
            print(robot.position.z)
            print(robot.speed)
            print(robot.current_energy)
            print('--------------------------------')"""

    def execute_faults(self):
        """ Check for fault """
        for fault in self.fault_specification:
            fault.exec_fault(self.time, self.sim_interface.mission)
            	
    def runCI(self, fs):
        self.reset_system_state(fs)
        # Run simulation
        for t in range(self.mission.duration):
        	self.update_system_state()
        	self.execute_faults()
        	self.check_avoidCollision()
        	self.check_stayWithinMissionArea()
        	self.check_sufficientEnergy()
        	self.check_gathersamples_g4()
        	self.check_gatherSamples_g5()
        	self.check_gatherSamples_g6()
        	t += 1
        	self.time = t
        print(self.goal_violations_per_fault)
        #print(self.total_goal_violations)
                
    def check_avoidCollision(self):
        # protected region User implemented method on begin
        goal_ID = "g1"
        """ Check if goal is violated and make a decision """
        collision_points = [[r.ID, r.position] for r in self.sim_interface.mission.robots.values()] + [[o.ID, o.area.center] for o in self.sim_interface.mission.obstacles.values()]
        for robot in self.sim_interface.mission.robots.values():
            for point in collision_points:
                if robot.ID != point[0] and robot.position == point[1]:
                    self.update_goal_violations(goal_ID)
                    robot.change_direction(robot.direction)
                    return False
        return True
		# protected region User implemented method end
		
    def check_stayWithinMissionArea(self):
        # protected region User implemented method on begin
        goal_ID = "g2"
        """ Check if goal is violated and make a decision """
        for robot in self.sim_interface.mission.robots.values():
            if robot.distance_from_mission_center(self.mission.mission_area.center) > self.sim_interface.mission.mission_area.radius:
                self.update_goal_violations(goal_ID)
                robot.change_direction(robot.direction)
                return False
        return True
		# protected region User implemented method end
		
    def check_sufficientEnergy(self):
        # protected region User implemented method on begin
        goal_ID = "g3"
        """ Check if goal is violated and make a decision """
        for robot in self.sim_interface.mission.robots.values():
            if not robot.check_for_sufficient_energy():
                self.update_goal_violations(goal_ID)
                self.sim_interface.mission.robots[robot.ID].update_speed(random.randint(robot.speed // 2, (robot.speed // 2) + 1))
                return False
        return True
		# protected region User implemented method end
		
    def check_gathersamples_g4(self):
        # protected region User implemented method on begin
        goal_ID = "g4"
        sensor = self.sim_interface.mission.goals[goal_ID].goalTask.sensor
        """ Check if goal is violated and make a decision """
        if sensor.state == "Active" and self.check_sufficientEnergy() and self.check_stayWithinMissionArea():
            if sensor.samples[len(sensor.samples) - 1] >= sensor.samples_per_second:
                g = self.sim_interface.mission.goals.get(goal_ID).goalTask
                g.total_samples += sensor.samples[len(sensor.samples) - 1]
        else:
            self.update_goal_violations(goal_ID)
		# protected region User implemented method end
		
    def check_gatherSamples_g5(self):
        # protected region User implemented method on begin
        goal_ID = "g5"
        sensor = self.sim_interface.mission.goals[goal_ID].goalTask.sensor
        """ Check if goal is violated and make a decision """
        if sensor.state == "Active" and self.check_sufficientEnergy() and self.check_stayWithinMissionArea():
            if sensor.samples[len(sensor.samples) - 1] >= sensor.samples_per_second:
                g = self.sim_interface.mission.goals.get(goal_ID).goalTask
                g.total_samples += sensor.samples[len(sensor.samples) - 1]
        else:
            self.update_goal_violations(goal_ID)
		# protected region User implemented method end
		
    def check_gatherSamples_g6(self):
        # protected region User implemented method on begin
        goal_ID = "g6"
        sensor = self.sim_interface.mission.goals[goal_ID].goalTask.sensor
        """ Check if goal is violated and make a decision """
        if sensor.state == "Active" and self.check_sufficientEnergy() and self.check_stayWithinMissionArea():
            if sensor.samples[len(sensor.samples) - 1] >= sensor.samples_per_second:
                g = self.sim_interface.mission.goals.get(goal_ID).goalTask
                g.total_samples += sensor.samples[len(sensor.samples) - 1]
        else:
            self.update_goal_violations(goal_ID)
		# protected region User implemented method end
		
    
    """
    def print_mission_and_fault_specification(self):
        self.reset_system_state(FaultSpecification(MissionLoader().load_mission()))
        # Setup mission specification
        print("Mission Specification")
        print(self.mission.name)
        print(self.mission.duration)
        print(self.mission.mission_area)
        print(self.mission.robots)
        print(self.mission.servers)
        print(self.mission.obstacles)
        print(self.mission.goals)

        print("\nFault Specification")
        print(self.fault_specification.faults)
        pop = self.fault_specification.generate_population()
        for i in range(len(pop)):
            s = ""
            print("INDIVIDUAL: " + str(i))
            for k in pop[i]:
                s += k.type.message.ID + "(" + str(k.start) + ", " + str(k.finish)+ ") "
            print(s)
            print("---------------------------------\n")
     """