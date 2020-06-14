#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
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


class BinaryMetric(Metric):

    """Docstring for BinaryMetric. """

    def __init__(self, config):
        """TODO: to be defined1. """
        Metric.__init__(self)
        self.output_freq_ = int(config['metric_freq'])
        self.sigmoid_ = float(config['sigmoid']) if 'sigmoid' in config else 1.0
        if self.sigmoid_ < 0:
            print ('sigmoid param {} should greater than zero'.format(self.sigmoid_))
        self.num_data_ = None
        self.name = None
        self.label_ = None
        self.weights = None
        self.sum_weights = None

    def init(self, test_name, metadata, num_data):
        self.name = test_name
        self.num_data_ = num_data
        self.label_ = metadata.labels()
        self.weights = metadata.weights()
        if self.weights is None:
            self.sum_weights = float(self.num_data_)
        else:
            self.sum_weights = sum(self.weights)

    def print(self, iter_n, score):
        sum_loss = 0.0
        for i in range(self.num_data_):
            prob = 1.0 / (1.0 + np.exp(-self.sigmoid_ * score[i]))
            weight = 1.0
            if self.weights is not None:
                weight = self.weights[i]
            sum_loss += self.loss_on_point(self.label_[i], prob) * weight
        print ("Iteration:%d, %s's %s: %f" % (
            iter_n, self.name, self.metric_name(), sum_loss / self.sum_weights))

    @abc.abstractmethod
    def loss_on_point(self, label, prob):
        pass

    @abc.abstractmethod
    def metric_name(self):
        pass


class BinaryLoglossMetric(BinaryMetric):

    """Docstring for BinaryLogLossMetric. """

    def __init__(self, config):
        """TODO: to be defined1. """
        BinaryMetric.__init__(self, config)

    def loss_on_point(self, label, prob):

        if label == 0:
            if 1.0 - prob > kEpsilon:
                return -np.log(1.0 - prob)
        else:
            if prob > kEpsilon:
                return -np.log(prob);
        return -np.log(kEpsilon);

    def metric_name(self):
        return 'log loss'
