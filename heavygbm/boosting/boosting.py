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
        self.models_ = []

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
        # TODO: no valid now
        self.valid_score_updater_ = []
        self.num_data_ = self.train_data_.num_data()
        # create buffer for gradients and hessians
        self.gradients_ = None  # [None] * self.num_data_
        self.hessians_ = None  # [None] * self.num_data_

        # get max feature index
        self.max_feature_idx_ = max([feature.feature_idx for feature in self.train_data_.features_])
        print (self.max_feature_idx_)

        # if need bagging, create buffer
        # TODO, bagging 暂时不实现

        self.fout = open(output_model_filename, 'w')

        self.model_to_string()


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
            if new_tree.num_leaves_ <= 1:
                print ('new_tree->num_leaves()={}, Cannot do any boosting for tree cannot split'.format(
                    new_tree.num_leaves_))
                break
            # Shrinkage by learning rate
            new_tree.shrinkage(float(self.config['learning_rate']))
            # update score
            print ('debug_update', self.train_score_updater_.score())
            self.update_score(new_tree)
            # TODO: self.update_bagging_score(new_tree)
            # print message for metric
            print ('debug_update', self.train_score_updater_.score())

            self.output_metric(iter_num + 1)
            # add model
            self.models_.append(new_tree)
            # write model to file on every iteration
            self.fout.write('Tree={}\n'.format(iter_num))
            self.fout.write(new_tree.to_string())
            self.fout.write('\n')

    def update_score(self, tree):
        # update training score
        self.train_score_updater_.add_score(self.tree_learner_)
        # TODO:update validation score

    def output_metric(self, iter_n):
        # print training metric
        for metric in self.training_metrics_:
            metric.print(iter_n, self.train_score_updater_.score())
        # TODO: print validation metric

    def model_to_string(self):
        self.fout.write('max_feature_idx={}\n'.format(self.max_feature_idx_))
        self.fout.write('sigmoid={:g}\n\n'.format(self.object_function_.sigmoid_))
        for i in range(len(self.models_)):
            self.fout.write('Tree={}\n'.format(i))
            self.fout.write(self.models_[i].to_string())
            self.fout.write('\n')



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
        return self.tree_learner_.train(self.gradients_, self.hessians_)




        
