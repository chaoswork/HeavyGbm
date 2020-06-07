#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
import pandas as pd

from .bin import BinMapper
from ..treelearner import Feature


class Metadata(object):

    """Docstring for Metadata. """

    def __init__(self):
        """TODO: to be defined1. """
        self.labels_ = None
        self.weights_ = None
        self.init_score_ = None

    def init_labels(self, num_data):
        self.labels_ = [None] * num_data

    def set_label_at(self, idx, label):
        self.labels_[idx] = label

    def labels(self):
        return self.labels_

    def weights(self):
        return self.weights_

    def init_score(self):
        return self.init_score_



class DataSet(object):

    """Docstring for DataSet. """

    def __init__(self, filename, max_bin=255, random_seed=42):
        """TODO: to be defined1. """
        self.filename = filename
        self.max_bin = int(max_bin)
        self.random_seed = random_seed

        self.text_readed = None
        self.meta_data_ = Metadata()
        self.sample_data = None
        self.used_feature_map_ = None
        self.features_ = None
        self.num_data_ = 0
        self.is_enable_sparse_ = True

    def num_data(self):
        return self.num_data_

    def num_features(self):
        return len(self.features_)

    def meta_data(self):
        return self.meta_data_

    def feature_at(self, idx):
        return self.features_[idx]

    def load_train_data(self):
        """TODO: Docstring for load_train_data.

        :arg1: TODO
        :returns: TODO

        """

        # LoadDataToMemory
        self.text_readed = pd.read_csv(self.filename, header=None)
        self.num_data_ = self.text_readed.shape[0]
        # SampleDataFromMemory
        self.sample_data = self.text_readed.sample(n=min(50000, self.text_readed.shape[0]))
        print (self.sample_data)
        # ConstructBinMappers
        self.construct_bin_mappers()
        # metadata_.InitLabel
        self.meta_data_.init_labels(self.num_data_)
        # ExtractFeaturesFromMemory
        self.extract_feature_from_memory()

    def construct_bin_mappers(self):
        """TODO: Docstring for construct_bin_mappers.
        :returns: TODO
        """
        labels = self.sample_data.iloc[:,0].tolist()
        sample_values = np.transpose(self.sample_data.iloc[:,1:].to_numpy())

        self.features_ = []
        # -1 means doesn't use this feature
        self.used_feature_map_ = [-1] * sample_values.shape[0]
        print (labels, sample_values)
        for i in range(sample_values.shape[0]):
            bin_mapper = BinMapper()
            bin_mapper.find_bin(sample_values[i], self.max_bin)
            if bin_mapper.is_trival():
                continue
            # map real feature index to used feature index
            self.used_feature_map_[i] = len(self.features_)
            # push new feature
            new_feature = Feature(i, bin_mapper, self.sample_data.shape[0], self.is_enable_sparse_)
            self.features_.append(new_feature)

    def extract_feature_from_memory(self):

        for i in range(self.num_data_):
            label = self.text_readed.iloc[i, 0]
            feature = self.text_readed.iloc[i, 1:].tolist()
            self.meta_data_.set_label_at(i, label)
            for (real_feat_idx, value) in enumerate(feature):
                feature_idx = self.used_feature_map_[real_feat_idx]
                if feature_idx >= 0:
                    # if is used feature
                    self.features_[feature_idx].push_data(i, value)

        for i in range(len(self.features_)):
            print (self.features_[i].bin_data_.data_)

