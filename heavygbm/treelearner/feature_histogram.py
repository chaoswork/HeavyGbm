#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..io import HistogramBinEntry
from ..utils import kEpsilon
from .split_info import SplitInfo

class FeatureHistogram(object):

    """Docstring for FeatureHistogram. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    def init(self, feature, feature_idx,
             min_num_data_one_leaf, min_sum_hessian_one_leaf, init_index):
        self.feature_idx_ = feature_idx
        self.init_index = init_index
        self.min_num_data_one_leaf_ = min_num_data_one_leaf
        self.min_sum_hessian_one_leaf_ = min_sum_hessian_one_leaf
        self.bin_data_ = feature.bin_data()
        self.num_bin_ = feature.num_bin()
        # store HistogramBinEntry
        self.data_ = [None] * self.num_bin_
        self.is_splittable_ = True

        self.sum_gradients_ = None
        self.sum_hessians_ = None

    def to_string(self):
        return '(feature_idx={}, init_index={}, min_num_data_one_leaf_={}, min_sum_hessian_one_leaf={}, sum_gradients={}, sum_hessians={}, is_splittable={}, data_={})'.format(
            self.feature_idx_, self.init_index, self.min_sum_hessian_one_leaf_,
            self.min_sum_hessian_one_leaf_, self.sum_gradients_, self.sum_hessians_,
            self.is_splittable_,
            [x.to_string() if x else 'None' for x in self.data_]
        )


    def set_is_splittable(self, value):
        self.is_splittable_ = value

    def is_splittable(self):
        return self.is_splittable_

    def construct(self, data_indices, num_data,
                  sum_gradients, sum_hessians,
                  ordered_gradients, ordered_hessians):
        self.num_data_ = num_data
        self.sum_gradients_ = sum_gradients
        self.sum_hessians_ = sum_hessians + 2 * kEpsilon
        self.data_ = self.bin_data_.construct_histogram(
            data_indices, num_data, self.num_bin_,
            ordered_gradients, ordered_hessians)

    def find_best_threshold(self):
        best_sum_left_gradient = float('nan')
        best_sum_left_hessian = float('nan')
        best_gain = -float('inf')
        best_left_count = 0
        best_threshold = self.num_bin_
        sum_right_gradient = 0.0
        sum_right_hessian = kEpsilon
        right_count = 0
        gain_shift = self.get_leaf_split_gain(self.sum_gradients_, self.sum_hessians_)
        self.is_splittable_ = False
        # from right to left, and we don't need data in bin0
        for t in reversed(range(1, self.num_bin_)):
            sum_right_gradient += self.data_[t].sum_gradients
            sum_right_hessian += self.data_[t].sum_hessians
            right_count += self.data_[t].cnt
            # if data not enough, or sum hessian too small
            if right_count < self.min_num_data_one_leaf_ or \
                    sum_right_hessian < self.min_sum_hessian_one_leaf_:
                continue
            left_count = self.num_data_ - right_count
            sum_left_hessian = self.sum_hessians_ - sum_right_hessian
            if left_count < self.min_num_data_one_leaf_ or \
                    sum_left_hessian < self.min_sum_hessian_one_leaf_:
                continue
            sum_left_gradient = self.sum_gradients_ - sum_right_gradient
            # current split gain
            current_gain = self.get_leaf_split_gain(sum_left_gradient, sum_left_hessian) + \
                self.get_leaf_split_gain(sum_right_gradient, sum_right_hessian)
            print ('debug', t, sum_left_gradient, sum_left_hessian,
                   self.get_leaf_split_gain(sum_left_gradient, sum_left_hessian),
                   sum_right_gradient, sum_right_hessian, 
                   self.get_leaf_split_gain(sum_right_gradient, sum_right_hessian),
                   current_gain, gain_shift)
            # gain is worst than no perform split
            if current_gain < gain_shift:
                continue
            # mark to is splittable
            self.is_splittable_ = True
            # better split point
            if current_gain > best_gain:
                best_left_count = left_count
                best_sum_left_gradient = sum_left_gradient
                best_sum_left_hessian = sum_left_hessian
                #  left is <= threshold, right is > threshold.  so this is t-1
                best_threshold = t - 1
                best_gain = current_gain
        if self.is_splittable_ == False:
            print ('[debug] set is_splittable False')
        # update split information
        output = SplitInfo()
        output.feature_idx = self.feature_idx_
        output.threshold = best_threshold
        output.left_output = self.calculate_splitted_leaf_output(
            best_sum_left_gradient, best_sum_left_hessian)
        output.left_count = best_left_count
        output.left_sum_gradient = best_sum_left_gradient
        output.left_sum_hessian = best_sum_left_hessian
        output.right_output = self.calculate_splitted_leaf_output(
            self.sum_gradients_ - best_sum_left_gradient,
            self.sum_hessians_ - best_sum_left_hessian)
        output.right_count = self.num_data_ - best_left_count
        output.right_sum_gradient = self.sum_gradients_ - best_sum_left_gradient
        output.right_sum_hessian = self.sum_hessians_ - best_sum_left_hessian
        output.gain = best_gain - gain_shift
        return output


    def calculate_splitted_leaf_output(self, sum_gradients, sum_hessians):
        return -(sum_gradients) / (sum_hessians)


    def get_leaf_split_gain(self, sum_gradients, sum_hessians):
        return (sum_gradients * sum_gradients) / (sum_hessians)

    def subtract(self, other):
        self.num_data_ -= other.num_data_
        self.sum_gradients_ -= other.sum_gradients_
        self.sum_hessians_ -= other.sum_hessians_
        for i in range(self.num_bin_):
            self.data_[i].cnt -= other.data_[i].cnt
            self.data_[i].sum_gradients -= other.data_[i].sum_gradients
            self.data_[i].sum_hessians -= other.data_[i].sum_hessians


