#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .feature_histogram import FeatureHistogram
from .leaf_splits import LeafSplits
from .data_partition import DataPartition


class TreeLearner(object):

    """Docstring for TreeLearner. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    @staticmethod
    def create_tree_learner(tree_type, config):
        if tree_type == 'serial':
            return SerialTreeLearner(config)


class SerialTreeLearner(TreeLearner):

    """Docstring for SerialTreeLearner. """

    def __init__(self, config):
        """TODO: to be defined1. """
        TreeLearner.__init__(self)
        self.data_partition_ = None
        self.is_feature_used_ = None
        self.historical_histogram_array_ = None
        self.smaller_leaf_histogram_array_ = None
        self.larger_leaf_histogram_array_ = None
        self.smaller_leaf_splits_ = None
        self.larger_leaf_splits_ = None
        self.ordered_gradients_ = None
        self.ordered_hessians_ = None
        self.is_data_in_leaf_ = None
        self.train_data_ = None

        self.num_leaves_ = int(config['num_leaves'])
        self.min_num_data_one_leaf_ = int(config['min_data_in_leaf'])
        self.min_sum_hessian_one_leaf_ = float(config['min_sum_hessian_in_leaf'])
        self.feature_fraction_ = float(config['feature_fraction'])

    def init(self, train_data):
        self.train_data_ = train_data
        self.num_data_ = self.train_data_.num_data()
        self.num_features_ = self.train_data_.num_features()
        # allocate the space for historical_histogram_array_
        self.historical_histogram_array_ = [None] * self.num_leaves_
        # 每一个节点，每一维特征都有一个histogram, 这个结构非常非常重要
        # historical_histogram_array_[i][j]代表第i个树节点，第j维特征的直方图
        # historical_histogram_array_[i][j] 内部可以找到该特征的最佳分裂阈值
        # historical_histogram_array_[i] 遍历j，可以找到每个树节点最佳分裂的特征是哪个
        # historical_histogram_array_遍历i，可以找到哪个节点是最佳分裂的树节点
        for i in range(self.num_leaves_):
            self.historical_histogram_array_[i] = []
            for j in range(self.train_data_.num_features()):
                new_histogram = FeatureHistogram()
                new_histogram.init(
                    self.train_data_.feature_at(j), j,
                    self.min_num_data_one_leaf_,
                    self.min_sum_hessian_one_leaf_)
                self.historical_histogram_array_[i].append(new_histogram)

        for i in range(self.num_leaves_):
            for j in range(self.train_data_.num_features()):
                print (i, j, self.historical_histogram_array_[i][j].feature_idx_)
            print ('-' * 10)

        #  push split information for all leaves
        # best_split_per_leaf_.push_back(SplitInfo());
        self.best_split_per_leaf_ = [None] * self.num_leaves_

        # initialize ordered_bins_ with nullptr
        # TODO:ordered_bin暂时先不考虑

        self.smaller_leaf_splits_ = LeafSplits(self.train_data_.num_features(),
                                               self.train_data_.num_data())

        # initialize data partition
        self.data_partition_ = DataPartition(self.num_data_, self.num_leaves_);

        self.is_feature_used_ = [None] * self.num_features_

        # initialize ordered gradients and hessians
        self.ordered_gradients_ = [None] * self.num_data_
        self.ordered_hessians_ = [None] * self.num_data_





