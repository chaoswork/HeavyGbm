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
        self.leaf_index_ = 0
        self.data_indices_ = None
        self.best_split_per_feature_ = []
        self.sum_gradients_ = None
        self.sum_hessians_ = None

        for i in range(self.num_feature_):
            split_info = SplitInfo()
            self.best_split_per_feature_.append(split_info)
            self.best_split_per_feature_[i].feature_idx = i

    def init_gh(self, gradients, hessians):
        """TODO: Docstring for init.

        :gradients: TODO
        :hessians: TODO
        :returns: TODO

        """
        self.num_data_in_leaf_ = self.num_data_
        self.leaf_index_ = 0
        self.data_indices_ = None
        self.sum_gradients_ = sum(gradients)
        self.sum_hessians_ = sum(hessians)
        for split_info in self.best_split_per_feature_:
            split_info.reset()

    def init_ldgh(self, leaf, data_partition, gradients, hessians):
        """TODO: Docstring for init.

        :arg1: TODO
        :returns: TODO

        """
        pass
