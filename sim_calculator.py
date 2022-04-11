# -*- coding: utf-8 -*-
"""
@author: littleHurt
"""
import numpy as np
import pandas as pd


# set input list for testing
list_m = [0.019913, 0.048773, 0.061145, 0.05907, 0.100311, 0.127246,
          0.102991, 0.096562, 0.117279, 0.022999, 0.1987, 0.044751]
list_n = [0.01045, 0.020796, 0.014002, 0.101529, 0.186078, 0.082598,
          0.02337, 0.269065, 0.18737, 0.043361, 0.051611, 0.009037]
list_x = [4.1e-05, 4.2e-05, 4.1e-05, 4.2e-05, 4.2e-05, 4.2e-05,
          4.1e-05, 0.32991, 0.41986, 0.24991, 0.0, 0.0]
list_y = [0.998551, 0.000144, 0.000143, 0.000142, 0.000142, 0.000142,
          0.000142, 0.000142, 0.000142, 0.000141, 0.000141, 2.8e-05]


# similarity
def sim_calculator(list_1, list_2):
    """
    Calculate the similarity from two input seires data.
    The method consider both similarities of cumulative percentage of quantity and time.
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
    n_length = len(list_1)
    # -----------------------------------------------------------------
    # STEP1. normalize input list and get length of data
    def get_cum_pctg_qty(list_input, n_length = n_length):
        
        list_STEP1 = np.array(list_input) / sum(list_input)
        list_STEP2 = []
        for n in range(0,n_length):
            list_STEP2.append( round(sum(list_STEP1[:n+1]), 6) )
        
        return list_STEP1, list_STEP2
    # End local function: get_cum_pctg_qty()
    list_11 = get_cum_pctg_qty(list_1)[0].round(6)
    list_12 = get_cum_pctg_qty(list_2)[0].round(6)
    
    # STEP2. get cumulative qty percentage from previous step.
    list_21 = get_cum_pctg_qty(list_1)[1]
    list_22 = get_cum_pctg_qty(list_2)[1]
    
    
    # STEP3. get difference between {list_21, list_11}
    list_31 = np.array(list_21) - np.array(list_22)
    list_32 = np.array(list_22) - np.array(list_21) 
    
    
    # STEP4. keep only positive value in {list_21, list_22}
    def get_diff(list_input, n_length = n_length):
        list_STEP4 = []
        for n in range(0,n_length):
            # rearrange item in list_31
            if list_input[n] < 0:
                list_STEP4.append( 0 )
            else:
                list_STEP4.append( list_input[n] )
        return list_STEP4
    # End local function: get_diff()
    
    list_41 = get_diff(list_31)
    list_42 = get_diff(list_32)
    
    
    # STEP5. compute distane and similarity of cumulative qty percentage
    # get numerator of distance calculation from {list_41, list_42}
    numerator_qty = sum(list_41) + sum(list_42)
    
    # get denominator of distance calculation from {list_21, list_22}
    denominator_qty = sum(list_21) + sum(list_22)
    
    # -----------------------------------------------------------------
    # STEP5. get cumulative time percentage from previous step.
    def get_cum_pctg_time(list_STEP1, list_STEP2, n_length = n_length):
        list_STEP5 = []
        pct_t = 1/n_length
        m = 0
        for n in range(0, n_length):
            if (n+1) == n_length:
                list_STEP5.append(1)
            else:
                if list_STEP2[n] >= (n+1)/n_length:
                    list_STEP5.append( round((n+1)/n_length + list_STEP1[n] * pct_t, 6) )
                    m = m + 1
                else:
                    list_STEP5.append( round(list_STEP2[m] * pct_t, 6) )
                        
        return list_STEP5
    # End local function: get_cum_pctg_time()
    
    list_51 = get_cum_pctg_time(list_11, list_21)
    list_52 = get_cum_pctg_time(list_12, list_22)
    
    
    # STEP6. get difference between {list_51, list_21}
    list_61 = np.array(list_51) - np.array(list_52)
    list_62 = np.array(list_52) - np.array(list_51) 
    
    
    # # STEP7. keep only positive value in {list_61, list_62}
    list_71 = get_diff(list_61)
    list_72 = get_diff(list_62)
    
    
    # STEP8. compute distane and similarity of cumulative time percentage
    # get numerator of distance calculation from {list_71, list_72}
    numerator_time = sum(list_71) + sum(list_72)
    
    # get denominator of distance calculation from {list_51, list_52}
    denominator_time = sum(list_51) + sum(list_52)
    
    # -----------------------------------------------------------------
    # STEP9. get score of similarity by (score_qty * score_time)
    list_time_pctg = []
    for n in range(0, n_length):
        list_time_pctg.append( round( (n+1)/n_length, 6) )
    
    
    def get_df_compare(list_STEP1, list_STEP2, list_time_pctg, list_STEP5):
        df_qty = pd.DataFrame({
            'qty_pctg': list_STEP1,
            'qty_pctg_cum': list_STEP2,
            'time_pctg': list_time_pctg,
            'time_pctg_cum': list_STEP5, })
        return df_qty
    
    # End local function: get_df_compare()
    df_compare_1 = get_df_compare(list_11, list_21, list_time_pctg, list_51)
    df_compare_2 = get_df_compare(list_12, list_22, list_time_pctg, list_52)
    score = round(1 - (numerator_qty + numerator_time) / (denominator_qty + denominator_time), 6)
    
    
    return score, df_compare_1, df_compare_2
    # End of function: sim_calculator()



# see results
print( sim_calculator(list_m, list_n)[0] ) # result = 0.827362
print( sim_calculator(list_x, list_y)[0] ) # result = 0.580132

# End
