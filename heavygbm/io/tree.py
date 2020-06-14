#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tree(object):

    """Docstring for Tree. """

    def __init__(self, max_leaves):
        """TODO: to be defined1.

        :max_leaves: TODO

        """
        self.max_leaves_ = max_leaves
        self.num_leaves_ = 0
        self.left_child_ = [None] * (self.max_leaves_ - 1)
        self.right_child_ = [None] * (self.max_leaves_ - 1)
        self.split_feature_ = [None] * (self.max_leaves_ - 1)
        self.split_feature_real_ = [None] * (self.max_leaves_ - 1)
        self.threshold_in_bin_ = [None] * (self.max_leaves_ - 1)
        self.threshold_ = [None] * (self.max_leaves_ - 1)
        self.split_gain_ = [None] * (self.max_leaves_ - 1)

        self.leaf_parent_ = [None] * (self.max_leaves_)
        self.leaf_value_ = [None] * (self.max_leaves_)

        # only one root
        self.num_leaves_ = 1
        self.leaf_parent_[0] = None

    def shrinkage(self, rate):
        for i in range(self.num_leaves_):
            before = self.leaf_value_[i]
            if before is not None:
                self.leaf_value_[i] *= rate
            print ('leaf_value_[{}] shrinkage from {} to {}'.format(
                i, before, self.leaf_value_[i]))


    def split(self, leaf, feature_idx, threshold_bin, real_feature,
              threshold, left_value, right_value, gain):
        #   0
        #  / \
        # -1 -2  new_node_idx = 1
        new_node_idx = self.num_leaves_ - 1
        # update parent info
        parent = self.leaf_parent_[leaf]
        if parent is not None:
            # 把要分裂的节点，id变成new_node_ix,
            # 比如leaf=1, 则表明-2要分裂(~leaf)
            #   0
            #  / \
            # -1  1
            # if cur node is left child
            if self.left_child_[parent] == ~leaf:
                self.left_child_[parent] = new_node_idx
            else:
                self.right_child_[parent] = new_node_idx

        # add new node
        self.split_feature_[new_node_idx] = feature_idx;
        self.split_feature_real_[new_node_idx] = real_feature;
        self.threshold_in_bin_[new_node_idx] = threshold_bin;
        self.threshold_[new_node_idx] = threshold;
        self.split_gain_[new_node_idx] = gain;

        # add two new leaves
        #      0
        #     / \
        #    -1  1
        #       / \
        #      -2 -3
        self.left_child_[new_node_idx] = ~leaf;
        self.right_child_[new_node_idx] = ~self.num_leaves_;

        # update new leaves
        self.leaf_parent_[leaf] = new_node_idx;
        self.leaf_parent_[self.num_leaves_] = new_node_idx;
        self.leaf_value_[leaf] = left_value;
        self.leaf_value_[self.num_leaves_] = right_value;

        self.num_leaves_ += 1
        print (self.to_string())
        return self.num_leaves_ - 1

    def to_string(self):
        def list_to_str(alist, sep=' '):
            return sep.join(['{:g}'.format(x) for x in alist])
        tree_str_list = []
        tree_str_list.append('num_leaves=%d' % self.num_leaves_)
        tree_str_list.append('split_feature=%s' % list_to_str(self.split_feature_real_[:self.num_leaves_ - 1]))
        tree_str_list.append('split_gain=%s' % list_to_str(self.split_gain_[:self.num_leaves_ - 1]))
        tree_str_list.append('threshold=%s' % list_to_str(self.threshold_[:self.num_leaves_ - 1]))
        tree_str_list.append('left_child=%s' % list_to_str(self.left_child_[:self.num_leaves_ - 1]))
        tree_str_list.append('right_child=%s' % list_to_str(self.right_child_[:self.num_leaves_ - 1]))
        tree_str_list.append('leaf_parent=%s' % list_to_str(self.leaf_parent_[:self.num_leaves_]))
        tree_str_list.append('leaf_value=%s' % list_to_str(self.leaf_value_[:self.num_leaves_]))
        tree_str_list.append('')
        tree_str_list.append('')
        return '\n'.join(tree_str_list)

    def leaf_output(self, leaf):
        return self.leaf_value_[leaf]
