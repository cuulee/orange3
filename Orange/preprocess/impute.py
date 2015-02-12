import copy

import numpy

import Orange.data
from Orange.statistics import distribution, basic_stats
from .transformation import Transformation

__all__ = ["ReplaceUnknowns", "Average"]


def is_continuous(var):
    return isinstance(var, Orange.data.ContinuousVariable)


def is_discrete(var):
    return isinstance(var, Orange.data.DiscreteVariable)


class ReplaceUnknowns(Transformation):
    def __init__(self, variable, value=0):
        super().__init__(variable)
        self.value = value

    def transform(self, c):
        return numpy.where(numpy.isnan(c), self.value, c)


class Average:
    def __call__(self, data, variable):
        variable = data.domain[variable]
        if is_continuous(variable):
            stats = basic_stats.BasicStats(data, variable)
            value = stats.mean
        elif is_discrete(variable):
            dist = distribution.get_distribution(data, variable)
            value = dist.modus()
        else:
            raise TypeError("Variable must be continuous or discrete")

        var = copy.copy(variable)
        var.compute_value = ReplaceUnknowns(variable, value)
        return var