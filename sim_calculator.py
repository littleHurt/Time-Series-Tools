# -*- coding: utf-8 -*-
"""
@author: littleHurt
"""
import numpy as np


# set input list for testing
list_m = [0.019913, 0.048773, 0.061145, 0.05907, 0.100311, 0.127246,
          0.102991, 0.096562, 0.117279, 0.022999, 0.1987, 0.044751]
list_n = [0.01045, 0.020796, 0.014002, 0.101529, 0.186078, 0.082598,
          0.02337, 0.269065, 0.18737, 0.043361, 0.051611, 0.009037]
list_x = [4.1e-05, 4.2e-05, 4.1e-05, 4.2e-05, 4.2e-05, 4.2e-05,
          4.1e-05, 0.32991, 0.41986, 0.24991, 0.0, 0.0]
list_y = [0.088571, 0.000142, 0.000141, 0.000140, 0.00014, 0.00014,
          0.000140,  0.00014, 0.000140, 0.000139, 0.000139, 2.8e-05]


# similarity
def sim_calculator(list_1, list_2):
    """
    Calculate the similarity from two input seires data.
    The idea of this measurement is modified from the following paper:
        "Product family formation by matching Bill-of-Materials trees".
            by Mohamed Kashkoush & Hoda ElMaraghy.
        CIRP Journal of Manufacturing Science and Technology.
            Volume 12, January 2016, Pages 1-13
    -------------------------------------------------------
    Input:
        list_{1,2} : (list)
            A pair of seires with same length which we want to compare the similarity,
    -------------------------------------------------------
    Output:
        score : (float)
            A float of similarity between two list.
    """
    # STEP1. normalize input list and get length of data
    list_11 = np.array(list_1) / sum(list_1)
    list_12 = np.array(list_2) / sum(list_2)
    n_length = len(list_1)
    
    
    # STEP2. get cumulative percentage from previous step.
    list_21 = []
    list_22 = []
    for n in range(0,n_length):
        list_21.append( sum(list_11[:n+1]) )
        list_22.append( sum(list_12[:n+1]) )
        
        
    # STEP3. get difference between {list_21, list_11}
    list_31 = np.array(list_21) - np.array(list_22)
    list_32 = np.array(list_22) - np.array(list_21)
    
    
    # STEP4. keep only positive value in {list_21, list_22}
    list_41 = []
    list_42 = []
    for n in range(0,n_length):
        # rearrange item in list_31
        if list_31[n] < 0:
            list_41.append( 0 )
        else:
            list_41.append( list_31[n] )
        
        # rearrange item in list_32
        if list_32[n] < 0:
            list_42.append( 0 )
        else:
            list_42.append( list_32[n] )
    
    
    # STEP5. compute distane and similarity
    # get numerator of distance calculation from {list_41, list_42}
    numerator = sum(list_41) + sum(list_42)
    
    # get denominator of distance calculation from {list_21, list_22}
    denominator = sum(list_21) + sum(list_22)
    
    # get score of similarity
    score = 1 - round(numerator / denominator, 6)
    
    return score
    # End of function: sim_calculator()



# see results
print( sim_calculator(list_m, list_n) ) # result = 0.933754
print( sim_calculator(list_x, list_y) ) # result = 0.510146

# End