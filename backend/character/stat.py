''' General representation of stats '''

from enum import Enum, auto
import itertools
import math


class Stats(Enum):
    """
    Contains math factors for each individual stat.
    base: the base value for each stat
    m_factor: ???
    m_scalar: ???
    """
    # todo: have a better docstring
    MAINSTAT = (340, 165, 0)
    DET = (340, 130, 0)
    CRIT = (380, 200, 400)
    DH = (380, 1250, 0)
    SPEED = (380, 130, 0)
    TEN = (380, 100, 0)
    PIE = (340, 150, 0)
    GCD = (2500, 1, 0)  # in milliseconds
    PRECISION = (1000, 1, 0)  # defaulting to 3 digits of precision

    def __init__(self, base, m_factor, m_scalar):
        self.base = base
        self.m_factor = m_factor
        self.m_scalar = m_scalar

class Stat():
    """
    For each stat, gives a multiplier. Also holds the value of each stat.
    """
    def __init__(self, stat, value):
        """
        :param stat: from Stats enum.
        :param value: the current value of the stat.
        """
        self.stat = stat
        self.value = value

    @classmethod
    def truncate(cls, val, precision=1000):
        '''
        Truncate numbers to the specified number of sigfigs
        :return: the truncated number
        '''
        return (precision + val) / precision

    @classmethod
    def multiply_and_truncate(cls, val, factor, precision=1000):
        '''
        Returns the truncated result of val * factor
        :return: the truncated product
        '''
        return math.floor(val * cls.truncate(factor, precision))

    def get_multiplier(self):
        """
        Calculates the multiplier based on the stat.
        :return: A floating point number representing the multiplier.
        """
        if self.stat == Stats.DH:
            return 1.25

        magic_num = 3300
        if self.stat == Stats.MAINSTAT:
            magic_num = 340  # don't ask me why dude
        delta = self.value - self.stat.base
        return self.stat.m_factor * delta // magic_num + self.stat.m_scalar

    def apply_stat(self, damage):
        '''
        Applies the stat's multiplier to a damage value
        :return: the modified damage number
        '''
        return self.multiply_and_truncate(damage, self.get_multiplier())

class ProbabalisticStat(Stat):
    """
    Derived from Stat class, used for stats that increase the chance of something happening
    such as critical hit and direct hit.
    p_factor: something
    p_scalar: something else
    """
    def __init__(self, stat, value):
        """
        :param stat: from Stats enum.
        :param value: the current value of the stat.
        :param p_factor: ???
        :param p_scalar: ???
        """
        super().__init__(stat, value)
        self.p_factor = 1
        self.p_scalar = 0
        if stat == Stats.CRIT:
            self.p_factor = 200
            self.p_scalar = 50
        elif stat == Stats.DH:
            self.p_factor = 550

    def get_p(self):
        """
        calculates p?
        :return: returns p?
        """
        delta = self.value - self.stat.base
        return (self.p_factor * delta // 3300 + self.p_scalar) / Stats.PRECISION.base
