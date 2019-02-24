#!/usr/bin/env python3
# Python 3.6
"""
from ship_fsm.ship_states import *
import logging
import hlt
logging.basicConfig(filename='output.log',level=logging.DEBUG)

class ShipState(Ship):
	def __init__(self, ship):
		self.ship = ship
		self.position = ship.position
		self.state = Harvesting(self.ship, self.position)
	
	def on_event(self, event):
		pass
		
	def turn(self):
		Harvesting(self.ship, self.position)
		
"""
