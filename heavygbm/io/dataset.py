#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
import pandas as pd

from .bin import BinMapper


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
        self.max_bin = int(max_bin)
        self.random_seed = random_seed

        self.meta_data = Metadata()
        self.sample_data = None

    def load_train_data(self):
        """TODO: Docstring for load_train_data.

        :arg1: TODO
        :returns: TODO

        """

        # LoadDataToMemory
        text_readed = pd.read_csv(self.filename, header=None)
        # SampleDataFromMemory
        self.sample_data = text_readed.sample(n=min(50000, text_readed.shape[0]))
        print (self.sample_data)
        # ConstructBinMappers
        self.construct_bin_mappers()
        # metadata_.InitLabel
        # ExtractFeaturesFromMemory

    def construct_bin_mappers(self):
        """TODO: Docstring for construct_bin_mappers.
        :returns: TODO
        """
        labels = self.sample_data.iloc[:,0].tolist()
        sample_value = np.transpose(self.sample_data.iloc[:,1:].to_numpy())
        print (labels, sample_value)
        for i in range(sample_value.shape[0]):
            bin_mapper = BinMapper()
            bin_mapper.find_bin(sample_value[i], self.max_bin)



