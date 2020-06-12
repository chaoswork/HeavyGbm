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

    def init(self):
        self.leaf_index_ = None
        for split_info in self.best_split_per_feature_:
            split_info.reset()


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
        只适用于部分数据场景
        :arg1: TODO
        :returns: TODO

        """
        self.leaf_index_ = leaf
        self.num_data_in_leaf_ , self.data_indices_ = data_partition.get_index_on_leaf(leaf)
        # print ('debug', self.data_indices_)
        # print ('debug', gradients)
        # print ('debug', hessians)
        self.sum_gradients_ = sum([gradients[idx] for idx in self.data_indices_])
        self.sum_hessians_ = sum([hessians[idx] for idx in self.data_indices_])
        for split_info in self.best_split_per_feature_:
            split_info.reset()

    def init_ldgh_sum(self, leaf, data_partition, sum_gradients, sum_hessians):
        """TODO: Docstring for init.
        只适用于部分数据场景
        :arg1: TODO
        :returns: TODO

        """
        self.leaf_index_ = leaf
        self.num_data_in_leaf_ , self.data_indices_ = data_partition.get_index_on_leaf(leaf)
        # print ('debug', self.data_indices_)
        # print ('debug', sum_gradients)
        # print ('debug', sum_hessians)
        self.sum_gradients_ = sum_gradients
        self.sum_hessians_ = sum_hessians
        for split_info in self.best_split_per_feature_:
            split_info.reset()

    def to_string(self):
        return '(num_feature_={}, num_data_in_leaf_={}, num_data_={}, leaf_index_={}, data_indices_={}, best_split_per_feature_={}, sum_gradients={}, sum_hessians={})'.format(
            self.num_feature_,
            self.num_data_in_leaf_,
            self.num_data_,
            self.leaf_index_,
            self.data_indices_,
            [x.to_string() for x in self.best_split_per_feature_],
            self.sum_gradients_,
            self.sum_hessians_)

