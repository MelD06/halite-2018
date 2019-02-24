#!/usr/bin/env python3
# Python 3.6
import hlt
from hlt import constants
from hlt.positionals import Direction
import math
from hlt.entity import ShipState
import random
#from ship_fsm.ship import ShipState
from strategy import *
# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging
logme = open("output.log","w")
logme.close()
logging.basicConfig(filename='output.log',level=logging.DEBUG)


def surroundings_are_occupied(game_map, location):
    surroundings =  location.get_surrounding_cardinals()
    if game_map[location].is_occupied:
        return True
    for position in surroundings:
        if game_map[position].is_occupied:
            return True
    return False

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.

mapsquarehalf = simplify_matrix(game, 4)


game.ready("MelBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    listofships = []
    for ship in me.get_ships():
        listofships.append(ShipState(ship, game, ship.id, ship.position, ship.halite_amount))


    #if not me.get_ships() or ((me.halite_amount >= game.turn_number*40) and me.halite_amount > 1000 and len(me.get_ships()) < 15) and not surroundings_are_occupied(game_map, me.shipyard.position):
    if not me.get_ships() or (me.halite_amount > 1000 and game.turn_number < 200) and not surroundings_are_occupied(game_map, me.shipyard.position):
        logging.info("SPAWN!")
        command_queue.append(me.shipyard.spawn())

    for ship in listofships:
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        #if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
        command_queue.append(ship.turn())

    # Send your moves back to the game environment, ending this turn.
    logging.info(str(command_queue))
    game.end_turn(command_queue)

