from .SubComponent import SubComponent

class MotionSource(SubComponent):
	
	def __init__(self, id, energy_per_distance_unit):
		self.ID = id
		self.energy_per_distance_unit = energy_per_distance_unit
	
	def get_energy_per_distance_unit(self):
		return self.energy_per_distance_unit
