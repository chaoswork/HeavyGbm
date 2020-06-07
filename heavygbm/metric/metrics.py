#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

kEpsilon = 1e-15

class Metric(object):

    """Docstring for Metric. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    @staticmethod
    def create_metric(metric_type, config):
        """TODO: Docstring for create_m.

        """
        if metric_type == 'binary_logloss':
            return BinaryLoglossMetric(config)
        else:
            return None


class BinaryLoglossMetric(Metric):

    """Docstring for BinaryLogLossMetric. """

    def __init__(self, config):
        """TODO: to be defined1. """
        Metric.__init__(self)

    @staticmethod
    def LossOnPoint(label, prob):
        if label == 0:
            if 1.0 - prob > kEpsilon:
                return np.log(1.0 - prob)
        else:
            if prob > kEpsilon:
                return -np.log(prob);
        return -np.log(kEpsilon);
