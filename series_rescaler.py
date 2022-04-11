# -*- coding: utf-8 -*-
"""
@author: littleHurt
"""

# set input list for testing
list_a = [5,43,107,180,243,104,233,432,104,562,148,698,117,479,174,24,743,432]
list_b = [2,5,12,15,7,29,178,63,50,8,37,315,55,23,44,23]
list_c = [1,4,11,1490,0,360,2000,14,10,55,53,21,6,3,50,41,512,0,11,0,2,12,]



# define function of rescaler 
def series_rescaler(list_raw, period_new):
    """
    Rescale the length of input list by specified integer and normalize values in the list.
    The rescaled lengrh is allow to over or less from original length of list.
    Note that the output list may still have tiny gap from 1.
    -------------------------------------------------------
    Input:
        list_raw : (list)
            A list which we want to rescale its length and normalize its values.
        
        period_new: (int)
            An integer that we use to rescale to raw list.
    -------------------------------------------------------
    Output:
        list_new : (list)
            A rescaled list.
    """
    
    num_raw_sum = sum(list_raw)
    list_input = []
    
    for i in range(0, len(list_raw)):
        list_input.append(list_raw[i] / num_raw_sum)
        
    list_new = []    
    for columns in range(1, period_new + 1):
        list_new.append(0.0)
        
    period = []
    for percent in range(1, period_new + 1):
        period.append(len(list_raw) * (percent / period_new))
        
    unit = 0.01
    unit_count = 0.01
    
    for w in range(len(list_raw)):
        while unit_count < w:
            indexs = 0
            for position in range((len(period))):
                if unit_count > period[position]:
                    indexs += 1
            list_new[indexs] += float(list_input[w] * unit)
            unit_count += 0.01
            
    for j in range(0,5):
        for i in range(len(list_new)):
            list_new[i] = round(list_new[i] * (1 / sum(list_new)), 6)
        
    return list_new
    # End of function: list_rescaler()


# get rescale list by list_{a,b,c}
print(len(list_a), len(list_b), len(list_c))
list_a1 = series_rescaler(list_a, 12)
list_b1 = series_rescaler(list_b, 12)
list_c1 = series_rescaler(list_c, 12)


# see results
print(list_a1)
print(list_b1)
print(list_c1)

# End
