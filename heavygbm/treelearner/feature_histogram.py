#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..io import HistogramBinEntry

class FeatureHistogram(object):

    """Docstring for FeatureHistogram. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    def init(self, feature, feature_idx,
             min_num_data_one_leaf, min_sum_hessian_one_leaf):
        self.feature_idx_ = feature_idx
        self.min_num_data_one_leaf_ = min_num_data_one_leaf
        self.min_sum_hessian_one_leaf_ = min_sum_hessian_one_leaf
        self.bin_data_ = feature.bin_data()
        self.num_bin_ = feature.num_bin()
        # store HistogramBinEntry
        self.data_ = [None] * self.num_bin_


