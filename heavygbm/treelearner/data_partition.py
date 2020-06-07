#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

class DataPartition(object):

    """Docstring for DataPartition. """

    def __init__(self, num_data, num_leaves):
        """TODO: to be defined1.

        :num_data: TODO
        :num_leaves: TODO

        """
        self.num_data_ = num_data
        self.num_leaves_ = num_leaves
        self.leaf_begin_ = [None] * self.num_leaves_
        self.leaf_count_ = [None] * self.num_leaves_
        self.indices_ = [None] * self.num_data_
        self.temp_left_indices_ = [None] * self.num_data_
        self.temp_right_indices_ = [None] * self.num_data_
        self.used_data_indices_ = None
        self.used_data_count_ = None

    def init(self):
        """
        Init, will put all data on the root(leaf_idx = 0)
        """
        self.leaf_count_ = [0] * self.num_leaves_
        self.leaf_begin_[0] = 0
        if self.used_data_indices_ is None:
            # if using all data
            self.leaf_count_[0] = self.num_data_
            self.indices_ = list(range(self.num_data_))
        else:
            # if bagging
            self.leaf_count_[0] = self.used_data_count_
            self.indices_ = copy.deepcopy(self.used_data_indices_)



        
