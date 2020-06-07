#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .split_info import SplitInfo

class LeafSplits(object):

    """Docstring for LeafSplits. """

    def __init__(self, num_feature, num_data):
        """TODO: to be defined1.

        :num_feature: TODO
        :num_data: TODO

        """
        self.num_feature_ = num_feature
        self.num_data_in_leaf_ = num_data
        self.num_data_ = num_data
        self.data_indices_ = None
        self.best_split_per_feature_ = []

        for i in range(self.num_feature_):
            split_info = SplitInfo()
            self.best_split_per_feature_.append(split_info)
            self.best_split_per_feature_[i].feature_idx = i

            
