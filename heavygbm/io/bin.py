#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class HistogramBinEntry(object):
    def __init__(self):
        # /*! \brief Sum of gradients on this bin */
        self.sum_gradients = 0.0
        # /*! \brief Sum of hessians on this bin */
        self.sum_hessians = 0.0
        # /*! \brief Number of data on this bin */
        self.cnt = 0


class BinMapper(object):

    """Docstring for BinMapper. """

    def __init__(self):
        """TODO: to be defined1. """
        self.num_bin_ = None
        self.bin_upper_bound_ = None
        self.is_trival_ = None
        self.sparse_rate_ = None

    def is_trival(self):
        """TODO: Docstring for is_trival.
        :returns: TODO

        """
        return self.is_trival_

    def num_bin(self):
        return self.num_bin_

    def sparse_rate(self):
        return self.sparse_rate_

    def find_bin(self, values_list, max_bin):
        distinct_values, counts = np.unique(values_list, return_counts=True)
        print (distinct_values, counts)
        cnt_in_bin0 = counts[0]
        if len(distinct_values) < max_bin:
            # use distinct value is enough
            self.num_bin_ = len(distinct_values)
            self.bin_upper_bound_ = [(0.0 + x + y) / 2 for x, y in zip(distinct_values[:-1], distinct_values[1:])]
            self.bin_upper_bound_.append(float('inf'))
            print (self.bin_upper_bound_)
        else:
            self.num_bin_ = max_bin
            self.bin_upper_bound_ = [None] * max_bin
            bin_lower_bound = [None] * max_bin
            mean_bin_size = float(len(values_list)) / max_bin
            rest_sample_cnt = len(values_list)
            cur_cnt_inbin = 0
            bin_cnt = 0
            bin_lower_bound[0] = distinct_values[0];
            for i in range(len(distinct_values) - 1):
                rest_sample_cnt -= counts[i]
                cur_cnt_inbin += counts[i]
                # need a new bin
                if cur_cnt_inbin >= mean_bin_size:
                    self.bin_upper_bound_[bin_cnt] = distinct_values[i]
                    if bin_cnt == 0:
                        cnt_in_bin0 = cur_cnt_inbin
                    bin_cnt += 1
                    bin_lower_bound[bin_cnt] = distinct_values[i + 1];
                    cur_cnt_inbin = 0
                    mean_bin_size = float(rest_sample_cnt) / (max_bin - bin_cnt)
            cur_cnt_inbin += counts[len(distinct_values) - 1];
            # update bin upper bound
            for i in range(bin_cnt):
                self.bin_upper_bound_[i] = (self.bin_upper_bound_[i] + bin_lower_bound[i + 1]) / 2.0;
            # last bin upper bound
            self.bin_upper_bound_[bin_cnt] = float('inf')
            bin_cnt += 1
            # if no so much bin
            if bin_cnt < max_bin:
                self.bin_upper_bound_ = self.bin_upper_bound_[:bin_cnt]
                self.num_bin_ = bin_cnt
            print (self.bin_upper_bound_)

        self.is_trival_ = self.num_bin_ <= 1
        self.sparse_rate_ = float(cnt_in_bin0) / len(values_list)

    def value_to_bin(self, value):
        # use binary search to find bin
        l = 0
        r = self.num_bin_ - 1
        while l < r:
            m = int((r + l - 1) / 2)
            if value <= self.bin_upper_bound_[m]:
                r = m
            else:
                l = m + 1
        return l

    def bin_to_value(self, bin_):
        return self.bin_upper_bound_[bin_]

class Bin(object):

    """Docstring for Bin. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    @staticmethod
    def create_bin(num_data, num_bin, sparse_rate, is_enable_sparse):
        """TODO: Docstring for create_bin.
        """
        kSparseThreshold = 0.8
        if sparse_rate > kSparseThreshold and is_enable_sparse:
            return Bin.create_sparse_bin(num_data, num_bin), True
        else:
            return Bin.create_dense_bin(num_data, num_bin), False

    @staticmethod
    def create_dense_bin(num_data, num_bin):
        """
        根据num_bin的大小，申请不同的bit位数，节省内存用，这里不使用该功能。
        """
        return DenseBin(num_data)

    @staticmethod
    def create_sparse_bin(num_data, num_bin):
        """
        根据num_bin的大小，申请不同的bit位数，节省内存用，这里不使用该功能。
        """
        # TODO: 暂时用DenseBin代替
        return DenseBin(num_data)



class DenseBin(Bin):

    """Docstring for DenseBin.
    核心数据是data_, 每一个特征都有个bin数据。
    data_[i] = j表明第i行的样本的bin_index是j
    """

    def __init__(self, num_data):
        """TODO: to be defined1. """
        Bin.__init__(self)
        self.num_data = num_data
        self.data_ = [None] * num_data

    def push(self, idx, value):
        self.data_[idx] = value

    def construct_histogram(self, data_indices, num_data, num_bin,
                            ordered_gradients, ordered_hessians):
        hist_bin_entrys = []
        for i in range(num_bin):
            entry = HistogramBinEntry()
            hist_bin_entrys.append(entry)

        for i in range(num_data):
            if data_indices is not None:
                # use part of data
                bin_value = self.data_[data_indices[i]]
            else:
                bin_value = self.data_[i]
            hist_bin_entrys[bin_value].sum_gradients += ordered_gradients[i]
            hist_bin_entrys[bin_value].sum_hessians += ordered_hessians[i]
            hist_bin_entrys[bin_value].cnt += 1
        for i in range(num_bin):
            print (i, hist_bin_entrys[i].sum_gradients,
                   hist_bin_entrys[i].sum_hessians, hist_bin_entrys[i].cnt)
        return hist_bin_entrys

    def split(self, threshold, data_indices):
        left_indices = [idx for idx in data_indices if self.data_[idx] <= threshold]
        right_indices = [idx for idx in data_indices if self.data_[idx] > threshold]

        return left_indices, right_indices





