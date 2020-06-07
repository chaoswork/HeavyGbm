#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..treelearner import TreeLearner
from .score_updater import ScoreUpdater

class Boosting(object):

    """Docstring for Boosting. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    @staticmethod
    def create_boosting(boosting_type, config):
        """TODO: Docstring for function.

        :arg1: TODO
        :returns: TODO

        """
        if boosting_type.upper() == 'GBDT':
            return GBDT(config)
        else:
            return None


class GBDT(Boosting):

    """Docstring for GBDT. """

    def __init__(self, config):
        """TODO: to be defined1. """
        Boosting.__init__(self)
        self.train_data_ = None
        self.tree_learner_ = None
        self.config = config

    def init(self, train_data, objective_function, train_metrics, output_model_filename):
        self.train_data_ = train_data
        # create tree learner
        self.tree_learner_ = TreeLearner.create_tree_learner(
            self.config['tree_learner'], self.config
        )
        # init tree learner
        self.tree_learner_.init(self.train_data_)
        self.object_function_ = objective_function
        # push training metrics
        self.training_metrics_ = []
        for metric in train_metrics:
            self.training_metrics_.append(metric)
        # create score tracker
        self.train_score_updater_ = ScoreUpdater(self.train_data_)
        self.num_data_ = self.train_data_.num_data()
        # create buffer for gradients and hessians
        self.gradients_ = None  # [None] * self.num_data_
        self.hessians_ = None  # [None] * self.num_data_

        # get max feature index
        self.max_feature_idx_ = max([feature.feature_idx for feature in self.train_data_.features_])
        print (self.max_feature_idx_)

        # if need bagging, create buffer
        # TODO, bagging 暂时不实现


    def train(self):
        for iter_num in range(int(self.config['num_trees'])):
            print ('iter#%d' % iter_num)
            # boosting first
            self.boosting()
            # Bagging logic
            self.bagging()
            # train a new tree
            new_tree = self.train_one_tree()
            # if cannon learn a new tree, stop
            # Shrinkage by learning rate
            # update score
            # print message for metric
            # add model
            # write model to file on every iteration


    def boosting(self):
        """
        计算一阶二阶导
        """
        self.gradients_, self.hessians_ = self.object_function_.get_gradients(
            self.train_score_updater_.score()
        )
        print (self.gradients_)
        print (self.hessians_)

    def bagging(self):
        pass

    def train_one_tree(self):
        pass




        
