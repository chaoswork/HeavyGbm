#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

class ObjectiveFunction(object):

    """Docstring for ObjectiveFunction. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    @staticmethod
    def create_objective_function(objective_type, config):
        """TODO: Docstring for create_objective_function.

        :objective_type: TODO
        :config: TODO
        :returns: TODO

        """
        if objective_type == 'binary':
            return BinaryLogloss(config)


class BinaryLogloss(ObjectiveFunction):

    """Docstring for BinaryLogLoss. """

    def __init__(self, config):
        """TODO: to be defined1. """
        ObjectiveFunction.__init__(self)
        self.label_val_ = [None] * 2
        self.label_weights_ = [None] * 2
        self.config = config
        self.sigmoid_ = self.config['sigmoid'] if 'sigmoid' in self.config else 1.0

    def init(self, meta_data, num_data):
        self.num_data_ = num_data
        self.labels = meta_data.labels()
        self.weights = meta_data.weights()

        cnt_positive = self.labels.count(1)
        cnt_negative = len(self.labels) - cnt_positive

        if cnt_positive == 0 or cnt_negative == 0:
            print ('input training data only contain one class')
            sys.exit(1)

        # use -1 for negative class, and 1 for positive class
        self.label_val_[0] = -1
        self.label_val_[1] = 1

        self.label_weights_[0] = 1.0
        self.label_weights_[1] = 1.0

        if 'is_unbalance' in self.config and self.config['is_unbalance'] == 'true':
            self.label_weights_[1] = 1.0 / cnt_positive
            self.label_weights_[0] = 1.0 / cnt_negative

    def get_gradients(self, score):
        gradients = []
        hessians = []
        for i in range(self.num_data_):
            label = self.label_val_[self.labels[i]]
            label_weight = self.label_weights_[self.labels[i]]
            # calculate gradients and hessians
            response = -2.0 * label * self.sigmoid_ / (1.0 + np.exp(2.0 * label * self.sigmoid_ * score[i]))
            grad = response * label_weight
            abs_response = np.fabs(response)
            hess = abs_response * (2.0 * self.sigmoid_ - abs_response) * label_weight
            if self.weights:
                grad = grad * self.weights[i]
                hess = hess * self.weights[i]

            gradients.append(grad)
            hessians.append(hess)

        return gradients, hessians





