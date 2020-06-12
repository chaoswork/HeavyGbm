#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SplitInfo(object):

    """Docstring for SplitInfo. """

    def __init__(self):
        """TODO: to be defined1. """
        self.feature_idx = None  # -1
        self.gain = -float('inf')
        self.threshold = None
        self.left_output = None  # Left output after split
        self.right_output = None
        self.left_count = None  # Left number of data after split
        self.right_count = None
        self.left_sum_gradient = None  # Left sum gradient after split
        self.right_sum_gradient = None
        self.left_sum_hessian = None  # Left sum hessian after split
        self.right_sum_hessian = None

    def reset(self):
        """
        threshold并没有改变。
        """
        self.feature_idx = None  # -1
        self.gain = -float('inf')

    def to_string(self):
        return '(feature_idx={}, gain={}, threshold={})'.format(
            self.feature_idx, self.gain, self.threshold
        )

