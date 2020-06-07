#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.used_data_indices_ = [None] * self.num_data_

        
