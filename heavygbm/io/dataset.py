#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


class Metadata(object):

    """Docstring for Metadata. """

    def __init__(self):
        """TODO: to be defined1. """
        pass


class DataSet(object):

    """Docstring for DataSet. """

    def __init__(self, filename, max_bin=255, random_seed=42):
        """TODO: to be defined1. """
        self.filename = filename
        self.max_bin = max_bin
        self.random_seed = random_seed

        self.meta_data = Metadata()
        self.sample_data = None

    def load_train_data(self):
        """TODO: Docstring for load_train_data.

        :arg1: TODO
        :returns: TODO

        """

        # LoadDataToMemory
        text_readed = open(self.filename).readlines()
        # SampleDataFromMemory
        self.sample_data = random.sample(text_readed, min(50000, len(text_readed)))
        print (self.sample_data[0])
        # ConstructBinMappers
        # metadata_.InitLabel
        # ExtractFeaturesFromMemory



