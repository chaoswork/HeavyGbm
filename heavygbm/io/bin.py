#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class BinMapper(object):

    """Docstring for BinMapper. """

    def __init__(self):
        """TODO: to be defined1. """
        self.num_bin_ = None
        self.bin_upper_bound_ = None
        self.is_trival_ = None
        self.sparse_rate_ = None

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












        
