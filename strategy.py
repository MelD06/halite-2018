#!/usr/bin/env python3
# Python 3.6
""" Basic strategy functions """
import hlt
import logging

def simplify_matrix(game, simplevel):
	""" Determines best areas to mine by simplifying the map to get a simple direction 
		Needs game object and simplification level (power of 2 cannot be higher than map_size (TODO : to be implemented) """
	mapsquarehalf = []
	premap = game.game_map
	for x in range(0,premap.width,simplevel):
		ouaiyes = []
		for y in range(0,premap.height,simplevel):
			sumof = 0
			for littlex in range(x,x+simplevel): #sums the smaller matrix
				for littley in range(y,y+simplevel):
					sumof += premap[hlt.entity.Position(littlex,littley)].halite_amount
			ouaiyes.append(sumof)
		mapsquarehalf.append(ouaiyes)
	#DEBUG
	logging.info(str(mapsquarehalf))
	return mapsquarehalf


def set_strategy_direction(ship_location):
	pass
	
