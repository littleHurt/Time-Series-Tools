# -*- coding: utf-8 -*-
"""
@author: littleHurt
"""
import math
import numpy as np

# define function of grey forecasting model
def grey_forecast(list_input, n = 1):
    """
    Implement grey forecasting model where is based on GM(l,l) of grey relational space.
    The idea of grey forecasting model is cited from following paper:
        "Introduction to Grey System Theory". by Deng Julong.
        The Journal of Grey System. Volume 1, issue 1, October 1989, pp1–24.
    # https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.678.3477&rep=rep1&type=pdf
    -------------------------------------------------------
    Input:
        list_input : (list)
            The training data which used to fit grey forecasting model.
            Require at least 2 values in the list.
            
        periods : (int)
            The number of future periods of forecasting values, default 1.
    -------------------------------------------------------
    Output:
        [0] prediction : (list)
            The forecastig value with specified periods.
            
        [1] Simulated values : (list)
            The simulated values of past.
            
        [2] Parameters : (tuple)
            The parameters from fitted model.
            
        [3] MSE : (float)
            Mean Square Error from fitted model.
            
        [4] MAE : (float)
            Mean Absolute Error from fitted model.
    """
    # create accumulative-generated series
    list_a = list(np.cumsum(list_input))
    
    
    # create mean-generated series
    list_b = []
    
    for i in range(1, len(list_input)):
        mean_acc = ( list_a[i-1] + list_a[i] ) / 2
        list_b.append( - mean_acc )
        
    # calculate the parameters of model
    bn = np.transpose(np.array([list_b, [1 for j in range(len(list_b))] ]))
    bnT = np.transpose(bn)
    
    Yn = np.array(list_input[1: len(list_input)])
    Yn = Yn.reshape(Yn.shape[0],1)
    
    MMULT_1 = np.dot(bnT, bn)
    MMULT_2 = np.dot(bnT, Yn)
    MMULT_1_invers = np.linalg.inv(MMULT_1)
    MMULT_3 = np.dot(MMULT_1_invers, MMULT_2 )
    
    a = MMULT_3[0][0]
    b = MMULT_3[1][0]
    params = (a,b)
    
    # create an empty list to store all forecasting value 
    list_pred = []
    
    # create an empty list to store all residuals
    list_residuals = []
    list_residuals_sqr = []
    
    # create formula of prediction 
    # x(k+1) = [ x(1) - b/a] *[ (math.e)^(-a*k) ] + b/a - x(k)
    # where x(k) is the k-th item of input series
   
    num_initial = list_input[0] - b/a
    for k in range(1, len(list_input) + (n + 1) ):
        if k == 1:
            num_pred = num_initial * ( math.e ** (-(a*k)) ) + b/a - list_input[0]
        else:            
            num_pred = num_initial * ( math.e ** (-(a*k)) ) + b/a - \
                (  num_initial * ( math.e ** (-(a*(k-1))) ) + b/a  )
        list_pred.append( num_pred )
        
        if k <= len(list_input):
            num_residuals_sqr = abs(num_pred - list_input[k-1])**2
            list_residuals_sqr.append(num_residuals_sqr)
            
            num_residuals = abs(num_pred - list_input[k-1])
            list_residuals.append(num_residuals)            
    
    # get prediction
    future_pred = list_pred[len(list_input):]
    past_simulated = list_pred[:len(list_input)]
    
    # calculate forecasting metrics
    MSE = sum(list_residuals_sqr) / len(list_input)
    MAE = sum(list_residuals) / len(list_input)
    
    return future_pred, past_simulated, params, MSE, MAE
# End of function


# set testing data
data = [44, 88, 50, 66, 77, 33, 33]


# see testing result
print(grey_forecast(data,3)[0]) # generate 3 stpes forecasting values
print(grey_forecast(data)[1]) # generate simulated value of input data
print(grey_forecast(data)[2]) # get parameters from fitted model.
print(grey_forecast(data)[3]) # get MSE from fitted model
print(grey_forecast(data)[4]) # get MAE from fitted model

# End
