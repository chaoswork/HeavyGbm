#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..io.bin import Bin

class Feature(object):

    """Docstring for Feature. """

    def __init__(self, feature_idx, bin_mapper, num_data, is_enable_sparse):
        """TODO: to be defined1. """
        self.feature_idx = feature_idx
        self.bin_mapper = bin_mapper
        self.bin_data, self.is_sparse = Bin.create_bin(
            num_data,
            bin_mapper.num_bin(),
            bin_mapper.sparse_rate(),
            is_enable_sparse
        )

        self.num_data = num_data
        self.is_enable_sparse = is_enable_sparse
        
