#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

from .feature_histogram import FeatureHistogram
from .leaf_splits import LeafSplits
from .split_info import SplitInfo
from .data_partition import DataPartition
from ..io import Tree


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
        self.ptr_to_ordered_gradients_ = None
        self.ptr_to_ordered_hessians_ = None

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
        self.hha_index = [None] * self.num_leaves_
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
                self.hha_index[i] = i

        for i in range(self.num_leaves_):
            for j in range(self.train_data_.num_features()):
                print (i, j, self.historical_histogram_array_[i][j].feature_idx_)
            print ('-' * 10)

        #  push split information for all leaves
        # best_split_per_leaf_.push_back(SplitInfo());
        self.best_split_per_leaf_ = []  # [None] * self.num_leaves_
        for i in range(self.num_leaves_):
            split_info = SplitInfo()
            self.best_split_per_leaf_.append(split_info)

        # initialize ordered_bins_ with nullptr
        # TODO:ordered_bin暂时先不考虑

        self.smaller_leaf_splits_ = LeafSplits(self.train_data_.num_features(),
                                               self.train_data_.num_data())
        self.larger_leaf_splits_ = LeafSplits(self.train_data_.num_features(),
                                              self.train_data_.num_data())

        # initialize data partition
        self.data_partition_ = DataPartition(self.num_data_, self.num_leaves_);

        self.is_feature_used_ = None  # [None] * self.num_features_

        # initialize ordered gradients and hessians
        self.ordered_gradients_ = [None] * self.num_data_
        self.ordered_hessians_ = [None] * self.num_data_


    def train(self, gradients, hessians):
        """TODO: Docstring for train.

        :gradients: TODO
        :hessians: TODO
        :returns: TODO

        """
        self.gradients_ = gradients
        self.hessians_ = hessians
        # some initial works before training
        self.before_train()
        tree = Tree(self.num_leaves_)
        # root leaf
        left_leaf = 0
        # only root leaf can be splitted on first time
        right_leaf = None

        for iter_split in range(self.num_leaves_ - 1):
            print ('iter_split=%d' % iter_split)
            # some initial works before finding best split, BeforeFindBestSplit
            if self.before_find_best_split(left_leaf, right_leaf):
                # find best threshold for every feature, FindBestThresholds
                self.find_best_thresholds()
                # find best split from all features, FindBestSplitsForLeaves
                self.find_best_splits_for_leaves()

            # 原始版本如果gain相同，则返回相同的index
            best_leaf = np.argmax([x.gain for x in self.best_split_per_leaf_])
            best_leaf_splitinfo = self.best_split_per_leaf_[best_leaf]
            if best_leaf_splitinfo.gain <= 0:
                break
            left_leaf, right_leaf = self.split(tree, best_leaf)


    def split(self, tree, best_leaf):
        best_split_info = self.best_split_per_leaf_[best_leaf]
        #  left = parent
        left_leaf = best_leaf
        feature_idx = best_split_info.feature_idx
        threshold = best_split_info.threshold
        assert self.train_data_.feature_at(feature_idx).feature_idx == feature_idx
        # split tree, will return right leaf
        right_leaf = tree.split(best_leaf, feature_idx, threshold,
                                self.train_data_.feature_at(feature_idx).feature_idx,
                                self.train_data_.feature_at(feature_idx).bin_to_value(threshold),
                                best_split_info.left_output, best_split_info.right_output,
                                best_split_info.gain)
        # split data partition
        self.data_partition_.split(best_leaf, self.train_data_.feature_at(feature_idx).bin_data(),
                                   threshold, right_leaf)

        # init the leaves that used on next iteration
        if best_split_info.left_count < best_split_info.right_count:
            self.smaller_leaf_splits_.init_ldgh_sum(
                left_leaf, self.data_partition_,
                best_split_info.left_sum_gradient,
                best_split_info.left_sum_hessian)
            self.larger_leaf_splits_.init_ldgh_sum(
                right_leaf, self.data_partition_,
                best_split_info.left_sum_gradient,
                best_split_info.left_sum_hessian)
        else:
            self.smaller_leaf_splits_.init_ldgh_sum(
                right_leaf, self.data_partition_,
                best_split_info.left_sum_gradient,
                best_split_info.left_sum_hessian)
            self.larger_leaf_splits_.init_ldgh_sum(
                left_leaf, self.data_partition_,
                best_split_info.left_sum_gradient,
                best_split_info.left_sum_hessian)

        print (left_leaf, right_leaf)
        return left_leaf, right_leaf



    def before_train(self):
        """TODO: Docstring for before_train.
        :returns: TODO

        """
        self.is_feature_used_ = [False] * self.num_features_
        used_feature_cnt = int(self.num_features_ * self.feature_fraction_)
        used_feature_indices = random.sample(list(range(self.num_features_)), used_feature_cnt)
        for idx in used_feature_indices:
            self.is_feature_used_[idx] = True
        # set all histogram to splittable
        for i in range(self.num_leaves_):
            for j in range(self.train_data_.num_features()):
                self.historical_histogram_array_[i][j].set_is_splittable(True)

        # initialize data partition
        self.data_partition_.init()

        # reset the splits for leaves
        for i in range(self.num_leaves_):
            self.best_split_per_leaf_[i].reset()
            print (self.best_split_per_leaf_[i].gain)

        # Sumup for root
        if self.data_partition_.leaf_count_[0] == self.num_data_:
            # use all data
            self.smaller_leaf_splits_.init_gh(self.gradients_, self.hessians_)
            # point to gradients, avoid copy
            self.ptr_to_ordered_gradients_ = self.gradients_
            self.ptr_to_ordered_hessians_ = self.hessians_
        else:
            # use bagging, only use part of data
            self.smaller_leaf_splits_.init_ldgh(0, self.data_partition_,
                                           self.gradients_, self.hessians_)
            _, data_indices = self.data_partition_.get_index_on_leaf(0)
            self.ordered_gradients_ = [self.gradients_[idx] for idx in data_indices]
            self.ordered_hessians_ = [self.hessians_[idx] for idx in data_indices]
            self.ptr_to_ordered_gradients_ = self.ordered_gradients_
            self.ptr_to_ordered_hessians_ = self.ordered_hessians_

        self.larger_leaf_splits_.init()

        # if has ordered bin, need to initialize the ordered bin
        # TODO: ordered bin暂不实现

    def before_find_best_split(self, left_leaf, right_leaf):
        """TODO: Docstring for before_find_best_split(left_leaf, right_leaf).
        :returns: TODO

        """
        num_data_in_left_child = self.data_partition_.leaf_count_[left_leaf] if left_leaf is not None else 0
        num_data_in_right_child = self.data_partition_.leaf_count_[right_leaf] if right_leaf is not None else 0
        # no enough data to continue
        if num_data_in_right_child < self.min_num_data_one_leaf_ * 2 \
                and num_data_in_left_child < self.min_num_data_one_leaf_ * 2:
            self.best_split_per_leaf_[left_leaf].gain = float('-inf')
            if right_leaf is not None:
                self.best_split_per_leaf_[right_leaf].gain = float('-inf')
            return False

        # None if only has one leaf. else equal the index of smaller leaf
        smaller_leaf = None

        if right_leaf is None:
            self.smaller_leaf_histogram_array_ = self.historical_histogram_array_[left_leaf]
            self.larger_leaf_histogram_array_ = None
        elif num_data_in_left_child < num_data_in_right_child:
            smaller_leaf = left_leaf
            # put parent(left) leaf's histograms into larger leaf's histgrams
            self.larger_leaf_histogram_array_ = self.historical_histogram_array_[left_leaf];
            self.smaller_leaf_histogram_array_ = self.historical_histogram_array_[right_leaf];
            # We will construc histograms for smaller leaf, and smaller_leaf=left_leaf = parent.
            # if we don't swap the cache, we will overwrite the parent's hisogram cache.
            # std::swap(historical_histogram_array_[left_leaf], historical_histogram_array_[right_leaf]);
            # TODO: Why Swap???
            self.historical_histogram_array_[left_leaf], self.historical_histogram_array_[right_leaf] = \
                self.historical_histogram_array_[right_leaf], self.historical_histogram_array_[left_leaf]
            self.hha_index[left_leaf], self.hha_index[right_leaf] = \
                self.hha_index[right_leaf], self.hha_index[left_leaf]
        else:
            smaller_leaf = right_leaf
            # put parent(left) leaf's histograms to larger leaf's histgrams
            self.larger_leaf_histogram_array_ = self.historical_histogram_array_[left_leaf];
            self.smaller_leaf_histogram_array_ = self.historical_histogram_array_[right_leaf];

        # init for the ordered gradients, only initialize when have 2 leaves
        if smaller_leaf is not None:
            _, data_indices = self.data_partition_.get_index_on_leaf(smaller_leaf)
            self.ordered_gradients_ = [self.gradients_[idx] for idx in data_indices]
            self.ordered_hessians_ = [self.hessians_[idx] for idx in data_indices]
            self.ptr_to_ordered_gradients_ = self.ordered_gradients_
            self.ptr_to_ordered_hessians_ = self.ordered_hessians_

        return True

    def find_best_thresholds(self):
        """
        For every Feature
        """
        for feature_index in range(self.num_features_):
            # feature is not used
            if self.is_feature_used_[feature_index] is False:
                continue
            # if parent(larger) leaf cannot split at current feature
            if self.larger_leaf_histogram_array_ is not None and \
                    self.larger_leaf_histogram_array_[feature_index].is_splittable() is False:
                self.smaller_leaf_histogram_array_[feature_index].set_splittable(False)
                continue

            # construct histograms for smaller leaf
            # if (ordered_bins_[feature_index] == nullptr)
            if True:
                self.smaller_leaf_histogram_array_[feature_index].construct(
                    self.smaller_leaf_splits_.data_indices_,
                    self.smaller_leaf_splits_.num_data_in_leaf_,
                    self.smaller_leaf_splits_.sum_gradients_,
                    self.smaller_leaf_splits_.sum_hessians_,
                    self.ptr_to_ordered_gradients_,
                    self.ptr_to_ordered_hessians_
                )
            # find best threshold for smaller child
            self.smaller_leaf_splits_.best_split_per_feature_[feature_index] = \
                self.smaller_leaf_histogram_array_[feature_index].find_best_threshold()
            # only has root leaf
            if self.larger_leaf_splits_ is None or self.larger_leaf_splits_.leaf_index_ is None:
                print('Only has root leaf, continue')
                continue

            # construct histgroms for large leaf, we initialize larger leaf as the parent,
            # so we can just subtract the smaller leaf's histograms
            self.larger_leaf_histogram_array_[feature_index].subtract(
                self.smaller_leaf_histogram_array_[feature_index])

            self.larger_leaf_splits_.best_split_per_feature_[feature_index] = \
                self.larger_leaf_histogram_array_[feature_index].find_best_threshold()

    def find_best_splits_for_leaves(self):
        self.find_best_split_for_leaf(self.smaller_leaf_splits_)
        self.find_best_split_for_leaf(self.larger_leaf_splits_)

    def find_best_split_for_leaf(self, leaf_splits):
        if leaf_splits is None or leaf_splits.leaf_index_ is None:
            return
        gains = []
        for i in range(len(leaf_splits.best_split_per_feature_)):
            print (i, leaf_splits.best_split_per_feature_[i].feature_idx, 
                   leaf_splits.best_split_per_feature_[i].gain)
            gains.append(leaf_splits.best_split_per_feature_[i].gain)
        best_feature_idx = np.argmax(gains)
        leaf = leaf_splits.leaf_index_
        self.best_split_per_leaf_[leaf] = leaf_splits.best_split_per_feature_[best_feature_idx]

        assert self.best_split_per_leaf_[leaf].feature_idx == best_feature_idx
        self.best_split_per_leaf_[leaf].feature_idx = best_feature_idx
        print (leaf, best_feature_idx, gains[best_feature_idx])

