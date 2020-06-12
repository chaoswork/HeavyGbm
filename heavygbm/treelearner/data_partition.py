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

    def get_index_on_leaf(self, leaf):
        begin = self.leaf_begin_[leaf]
        end = begin + self.leaf_count_[leaf]
        indices = self.indices_[begin: end]
        return self.leaf_count_[leaf], indices

    def split(self, leaf, feature_bins, threshold, right_leaf):
        begin = self.leaf_begin_[leaf]
        cnt = self.leaf_count_[leaf]

        left_split, right_split = feature_bins.split(
            threshold, self.indices_[begin: begin + cnt])
        # print ('debug', left_split, right_split, self.indices_)
        self.indices_[begin: begin + len(left_split)] = left_split
        self.indices_[begin + len(left_split): begin + cnt] = right_split
        # print ('debug', left_split, right_split, self.indices_)

        # update leaf boundary
        self.leaf_count_[leaf] = len(left_split)
        self.leaf_begin_[right_leaf] = begin + len(left_split)
        self.leaf_count_[right_leaf] = cnt - len(left_split)


