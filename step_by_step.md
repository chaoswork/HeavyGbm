before iter:
    tree_split:
    0
    num_leaves = 1
iter_split=0, left_leaf = 0, right_leaf = -1
    smaller_leaf(leaf_index=0)_split stores all data
    larger_leaf_split(leaf_index=None)
    smaller_leaf_histogram_array_ = hha[0],
        feature0_bin_count=[(0,6,6), (0,4,4), (0,4,4), (0,6,6)]
        feature1_bin_count=[(-1,1,1), (0,4,4), (0,4,4), (1,1,1), (0,2,2), (0,4,4), (0,4,4)]
    hist:
    |0|1|2|3|4|5|
    |s|
    |0|1|2|3|4|5|
    best_split: smaller, feature_idx=1, gain = 1*1/1 + 1*1/19 - 0, best_threshold = 0
    tree_split:
      0
     / \
 -1(1) -2(19)
   L     S
    num_leaves = 2

iter_split=1, left_leaf=0, right_leaf=1,
    smaller_leaf_split(leaf_index=0) stores [18], sum_g = -1, sum_h = 1, 
    larger_leaf_split(leaf_index=1) store [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19], sum_g=1, sum_h=19
    smaller_leaf_histogram_array_ = hha[1],
        feature0_bin_count=[(0,0,0), (0,0,0), (0,0,0), (-1,1,1)]
        feature1_bin_count=[(-1,1,1), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0)]
    larger_leaf_histogram_array_ = hha[0],
        feature0_bin_count=[(0,6,6), (0,4,4), (0,4,4), (1,5,5)]
        feature1_bin_count=[(0,0,0), (0,4,4), (0,4,4), (1,1,1), (0,2,2), (0,4,4), (0,4,4)]
    hist:
    |0|1|2|3|4|5|
    |L|S|
    |1|0|2|3|4|5|
    |S|L|
    best_split: larger, feature_idx=0, gain = 1*1/5 - 1*1/19, best_threshold = 2
    tree_split:
        0         0            0
       / \       / \          / \
      -1 -2  => -1  1  => -1(1)  1(19)
                                / \
                           -2(14) -3(5)
                             L     S
    num_leaves=3 

iter_split=2, left_leaf=1, right_leaf=2,
    smaller_leaf_split(leaf_index=2) store [2, 9, 10, 17, 19], sum_g=1, sum_h=5
    larger_leaf_split(leaf_index=1) store [0,1,3,4,5,6,7,8,11,12,13,14,15,16], sum_g=0, sum_h=14
    smaller_leaf_histogram_array_ = hha[2],
        feature0_bin_count=[(0,0,0), (0,0,0), (0,0,0), (1,5,5)]
        feature1_bin_count=[(0,0,0), (-1,1,1), (-1,1,1), (0,0,0), (1,1,1), (1,1,1), (1,1,1)]
    larger_leaf_histogram_array_ = hha[1],
        feature0_bin_count=[(0,6,6), (0,4,4), (0,4,4), (0,0,0)]
        feature1_bin_count=[(0,0,0), (1,3,3), (1,3,3), (1,1,1), (-1,1,1), (-1,3,3), (-1,3,3)]
    hist:
    |1|0|2|3|4|5|
    | |L|S|
    best_split: smaller, feature=0, gain= 2*2/2+9/3 - 0.2=4.8, best_threshold=3
    tree split:
         0                   0                    0
        / \                 / \                  / \
    -1(1)  1(19)   =>   -1(1)  1(19)    =>   -1(1)  1(19)
          / \                 / \                  / \
     -2(14) -3(5)        -2(14)  2(5)         -2(14)  2(5)
                                                     / \
                                                 -3(2) -4(3)
    num_leaves = 4


iter_split=3, left_leaf=2, right_leaf=3
    smaller_leaf_split(leaf_index=2) store []
    larger_leaf_split(leaf_index=3) store []




