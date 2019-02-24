#!/usr/bin/env python3
# Python 3.6
from ship_fsm.state import State
import hlt
from hlt.positionals import Direction
import logging
import random

logging.basicConfig(filename='output.log', level=logging.DEBUG)
""" Defines ship's states """


class Homing(State):
    """ The ship is aiming for the nearest dropoff """

    def __init__(self, ship, game):
        self.ship = ship
        self.game = game
        self.next_move = hlt.commands.STAY_STILL

    def __str__(self):
        return self.ship.move(self.next_move)

    def _get_homing_next_move(self, shippos, gmap):
        drops = self.game.me.get_dropoffs()
        drops.append(self.game.me.shipyard)  # trying to add shipyard
        near_drop = drops[0]
        for drop in drops:
            if gmap.calculate_distance(shippos, drop.position) < gmap.calculate_distance(shippos, near_drop.position):
                near_drop = drop
        return Direction.convert(gmap.naive_navigate(self.ship, near_drop.position))

    @staticmethod
    def _is_on_dropoff(shippos, game):
        for drop in game.me.get_dropoffs():
            if drop.position == shippos:
                return True
            else:
                return False

    def do_turn(self):
        logging.info("Homing: Dropoffs : " + str(self.game.me.get_dropoffs()))
        if self._is_on_dropoff(self.ship.position, self.game):
            return self.ship.move(self.next_move)
        else:
            return self.ship.move(self._get_homing_next_move(self.ship.position, self.game.game_map))


class Seeking(State):
    """ The ship is moving to a designated harvest point """
    pass


class Harvesting(State):
    """ The ship is harvesting halite in the area until it's full """

    def __init__(self, ship, game):
        self.ship = ship
        self.game = game
        self.next_move = hlt.commands.STAY_STILL

    def __str__(self):
        return self.ship.move(self.next_move)

    def do_turn(self):
        if self.ship.position == self.game.me.shipyard.position:
            return self.ship.move(self._get_random_unoccupied_direction(self.ship, self.game.game_map))
        return self.ship.move(self._get_harvest_next_move(self.ship, self.game.game_map))

    @staticmethod
    def _get_harvest_next_move(shipp, gmap):
        surroundings = shipp.position.get_surrounding_cardinals()
        surroundings.append(shipp.position)
        # surroundings contains values in this order: NSEW
        # Now getting halite from each position
        sur_halite = {0: gmap[surroundings[0]].halite_amount,
                      1: gmap[surroundings[1]].halite_amount,
                      2: gmap[surroundings[2]].halite_amount,
                      3: gmap[surroundings[3]].halite_amount,
                      4: gmap[surroundings[4]].halite_amount}
        # Determining best move, if moving is ensuring gain or not
        gain_still = 0.25 * gmap[shipp.position].halite_amount
        lost_still = -0.10 * gmap[shipp.position].halite_amount
        best_move = 4
        for direction, value in sur_halite.items():
            if lost_still + 0.25 * value > gain_still:
                best_move = direction
        logging.info(
            "Harvest Info : Surroundings" + str(best_move) + "//" + str(sur_halite) + "//" + str(shipp.position))
        return gmap.naive_navigate(shipp, surroundings[best_move])

    # Used to prevent Ships from staying at shipyard if on conflicting tracks with other ships Homing,
    # In short : MOVE AWAY YOU DUMBFUCK !!!
    # Note : looks really similar to naive_navigate...
    @staticmethod
    def _get_random_unoccupied_direction(shipp, game_map):
        navigates = [Direction.Still]
        for solution in shipp.position.get_surrounding_cardinals():
            if not game_map[solution].is_occupied:
                navigates.append(game_map.naive_navigate(shipp, solution))
        return random.choice(navigates)


"""" The ship is creating a dropoff at its current location """


class DropoffSt(State):

    def __init__(self, ship, game):
        self.ship = ship
        self.game = game
        self.next_move = self.ship.make_dropoff()
        logging.info("Dropoff init")

    def __str__(self):
        return self.next_move

    def do_turn(self):
        return self.next_move
