import abc

from ship_fsm.ship_states import *
from . import commands, constants
from .positionals import Direction, Position
from .common import read_input
#Lib modified with Shipstate !!!

class Entity(abc.ABC):
    """
    Base Entity Class from whence Ships, Dropoffs and Shipyards inherit
    """
    def __init__(self, owner, id, position):
        self.owner = owner
        self.id = id
        self.position = position

    @staticmethod
    def _generate(player_id):
        """
        Method which creates an entity for a specific player given input from the engine.
        :param player_id: The player id for the player who owns this entity
        :return: An instance of Entity along with its id
        """
        ship_id, x_position, y_position = map(int, read_input().split())
        return ship_id, Entity(player_id, ship_id, Position(x_position, y_position))

    def __repr__(self):
        return "{}(id={}, {})".format(self.__class__.__name__,
                                      self.id,
                                      self.position)


class Dropoff(Entity):
    """
    Dropoff class for housing dropoffs
    """
    pass


class Shipyard(Entity):
    """
    Shipyard class to house shipyards
    """
    def spawn(self):
        """Return a move to spawn a new ship."""
        return commands.GENERATE


class Ship(Entity):
    """
    Ship class to house ship entities
    """
    def __init__(self, owner, id, position, halite_amount):
        super().__init__(owner, id, position)
        self.halite_amount = halite_amount

    @property
    def is_full(self):
        """Is this ship at max halite capacity?"""
        return self.halite_amount >= constants.MAX_HALITE

    def make_dropoff(self):
        """Return a move to transform this ship into a dropoff."""
        return "{} {}".format(commands.CONSTRUCT, self.id)

    def move(self, direction):
        """
        Return a move to move this ship in a direction without
        checking for collisions.
        """
        raw_direction = direction
        if not isinstance(direction, str) or direction not in "nsewo":
            raw_direction = Direction.convert(direction)
        return "{} {} {}".format(commands.MOVE, self.id, raw_direction)

    def stay_still(self):
        """
        Don't move this ship.
        """
        return "{} {} {}".format(commands.MOVE, self.id, commands.STAY_STILL)

    @staticmethod
    def _generate(player_id):
        """
        Creates an instance of a ship for a given player given the engine's input.
        :param player_id: The id of the player who owns this ship
        :return: The ship id and ship object
        """
        ship_id, x_position, y_position, halite = map(int, read_input().split())
        return ship_id, Ship(player_id, ship_id, Position(x_position, y_position), halite)

    def __repr__(self):
        return "{}(id={}, {}, cargo={} halite)".format(self.__class__.__name__,
                                                       self.id,
                                                       self.position,
                                                       self.halite_amount)


def _is_on_dropoff(shippos, game):
    for drop in game.me.get_dropoffs():
        if drop == shippos:
            return True
        else:
            return False


def dist_to_nearest_dropoff(shippos, game):
    drops = game.me.get_dropoffs()
    drops.append(game.me.shipyard)
    shortdist = 1000
    nrdrop = drops[0]
    for drop in drops:
        dropdist = game.game_map.calculate_distance(shippos, drop.position)
        if dropdist < shortdist :
            shortdist = dropdist
            nrdrop = drop.position
    return [shortdist, nrdrop]


class ShipState(Ship):
    def __init__(self, ship, game, shid, pos, halite):
        super(ShipState, self).__init__(ship, shid, pos, halite)
        self.ship = ship
        self.game = game
        self.position = pos
        self.state = Harvesting(self, self.game)

    def turn(self):
        nr_dropoff = dist_to_nearest_dropoff(self.ship.position, self.game)
        '''#if self.ship.is_full and (self.ship.id == 0 or self.ship.id == 1):
        #    self.state = DropoffSt(self, self.game)
        #if self.ship.is_full and nr_dropoff[0] > 8 and self.game.me.halite_amount > 4000: #Adding dropoff if too far
        #    self.state = DropoffSt(self, self.game)
        #elif self.ship.is_full and type(self.state) == Harvesting and self.game.me.get_dropoffs():'''
        """https://forums.halite.io/t/how-many-turns-are-there-in-a-game/629"""
        if self.ship.halite_amount > 850 and type(self.state) == Harvesting:
            self.state = Homing(self, self.game)
        elif self.game.turn_number > (300+(25*self.game.game_map.width)/8)-15:
            if self.ship.halite_amount < 100:
                self.state = Harvesting(self, self.game)
            elif type(self.state) == Harvesting and self.ship.halite_amount > 500:
                self.state = Homing(self, self.game)
        elif type(self.state) == Homing and _is_on_dropoff(self.ship.position, self.game):
            self.state = Harvesting(self, self.game)
        logging.info("Ship:" + str(self.ship.id) + " is on " + str(type(self.state)))
        logging.info(str(self.game.me.halite_amount)+"pose")

        return str(self.state.do_turn())

