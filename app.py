#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse


from heavygbm.io import DataSet
from heavygbm.metric import Metric
from heavygbm.boosting import Boosting
from heavygbm.objective import ObjectiveFunction
from heavygbm.treelearner import TreeLearner

class App(object):

    """
    Application
    """

    def __init__(self, argv):
        """
        init heavygbm
        """
        self.train_data_ = None
        self.train_metric_ = []
        self.config_ = self.load_parameters(argv)

    def load_parameters(self, argv):
        """TODO: Docstring for load_parameters.

        :argv: TODO
        :returns: TODO

        """
        parser = argparse.ArgumentParser(description='Parse command line')
        parser.add_argument('--config', dest='config_file', required=True,
                            action='store', help='config file')
        args = parser.parse_args(argv[1:])

        config = {}
        with open(args.config_file, 'r') as f:
            for line in f:
                segs = line.strip().split('=')
                if len(segs) != 2:
                    continue
                config[segs[0].strip()] = segs[1].strip()

        return config

    def load_data(self):
        # load train
        self.train_data_ = DataSet(self.config_['data'],
                                   max_bin=self.config_['max_bin'])
        self.train_data_.load_train_data()
        # create training metric
        if self.config_['is_training_metric'] == 'true':
            for metric_type in self.config_['metric'].split(','):
                metric_type = metric_type.strip()
                metric = Metric.create_metric(metric_type, self.config_)
                metric.init("training", self.train_data_.meta_data_, self.train_data_.num_data_)
                self.train_metric_.append(metric)
                print (self.train_metric_)


        # load valid

    def init_train(self):
        # create boosting
        self.boosting =  Boosting.create_boosting(
            self.config_['boosting_type'], self.config_)
        # create object function
        self.objective_func_ = ObjectiveFunction.create_objective_function(
            self.config_['objective'], self.config_
        )

        self.load_data()
        self.objective_func_.init(self.train_data_.meta_data(),
                                 self.train_data_.num_data())

        # boosting.init
        self.boosting.init(
            self.train_data_, self.objective_func_,
            self.train_metric_, self.config_['output_model']
        )
        # add validation data into boosting
        # TODO: 暂不实现

    def train(self):
        # boosting.train
        self.boosting.train()



if __name__ == "__main__":
    import sys
    app = App(sys.argv)
    print(app.config_['task'])
    print(app.config_['num_leaves'])
    app.init_train()
    app.train()