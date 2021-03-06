#----------------#
# Import modules #
#----------------#

import itertools as it
import more_itertools as mit

import numpy as np

#------------------#
# Define functions #
#------------------#

def count_consecutive(array, calculate_max_consec=False):
    
    # Function that counts:
    #   1 : consecutive numbers in an array or pandas series,
    #       also distinguishing them by blocks.
    #   2 : maximum consecutive number subset length
    #       starting from an array that already satisfies certain condition,
    #       i.e. boolean array.
    
    # Example 1
    # ---------
    # random_list = [45, 46, 47, 48, 80, 81, 83, 87]
    # 
    # As can be seen, the first four numbers are consecutive,
    # it stops there and another two consecutive number sequence begins.
    # 
    # The result is then the following array:
    # consec_array = [4, 2]
    # 
    # Example 2
    # ---------
    # bool_array = [False, False, True, True, True, True, True, False, True, True]
    # consec_array = [5, 2]
    # max_consec_num = 5
    
    if not calculate_max_consec:
        
        consec_array_byGroups_lengths\
        = [len(list(group)) for group in mit.consecutive_groups(array)]
        
        if len(consec_array_byGroups_lengths) > 1:
            consec_array_byGroups_lengths_gt1\
            = [lng for lng in consec_array_byGroups_lengths if lng >1]
            return consec_array_byGroups_lengths_gt1
            
        elif len(consec_array_byGroups_lengths) == 1:
            return consec_array_byGroups_lengths
        
        else:
            return None
    
    else:
    
        bool_groups = [list(group) for _, group in it.groupby(array)]
        
        consec_array_byGroups_lengths_gt1\
        = [len(group) for group in bool_groups if group[0] and len(group)>1]
        
        if len(consec_array_byGroups_lengths_gt1) > 0:
            max_consec_num = np.max(consec_array_byGroups_lengths_gt1)
            return max_consec_num
        else:
            return None
        
def insert_values(x, index, values, axis=None):
    
    # Inserts values at the specified index either on a list or numpy array.
    # 
    # Parameters
    # ----------
    # x : list or numpy.ndarray
    #       Object containing whatever type of data
    # index : int
    #       Position where to introduce new data.
    #       Same behavior as introducing a blank space at the left
    #       and then filling it with new data.
    # values : list, numpy.array or pandas.core.series.Series
    #       If values are part of a data frame, they equally can be introduced
    #       into a list, to then call its data in the appropriate manner.
    # axis : int or NoneType
    #       Axis along which to insert 'values'.  If 'axis' is None then 'x'
    #       is flattened first.
    # 
    # Returns
    # -------
    # appended_array : numpy.ndarray
    #       Only ix 'x' is a numpy.ndarray. Array with new data appended.
    
    lx = len(x)
    
    if isinstance(x, list):        
        if index >= lx:
            print(f"Index {index} beyond list length, "
                  "will be appended at the end of it.")
            
        x.insert(index, values)
        return x
        
    elif isinstance(x, np.ndarray):
        x_appended = np.insert(x, index, values, axis=axis)
        return x_appended
        
    else:
        raise TypeError("Wrong type of data. "
                        "Data must either be a list or numpy array.")
        
def decompose_24h_cumulative_data(array, zeros_dtype='d'):
    
    # Function that obtains the 1-hour time step cumulative data,
    # subtracting to the next cumulative data, the previous cumulative value.
    # It is only intended for 24-hour time step hourly data.
    # 
    # The methodology, by its nature, gives negative values every 24 hours.
    # Assuming that data follow a cumulative distribution
    # and is definite positive, then those negative values
    # are considered as spurious and they are substituted by
    # arrays of zeroes.
    # It suffices to encounter a single negative value
    # along the n-1 dimensional array (for a time index) to set it to zero.
    # 
    # Parameters
    # ----------
    # array : numpy.ndarray
    #       Multi-dimensional array which contains data,
    #       being the first index corresponding to ??time?? dimension.
    # zeros_dtype : str or numpy type (e.g. numpy.int, numpy.float64)
    #       Sets the precision of the array composed of zeroes.
    # 
    # Returns
    # -------
    # hour_TS_array : numpy.ndarray
    #       Multi dimensional array containing
    #       1-hour time step cumulative data.
    
    records = len(array)
    array_shape = array.shape
    
    unmet_case_values = np.zeros(array_shape, dtype=zeros_dtype)
    
    hour_TS_array\
    = np.array([array[t+1] - array[t]
                if np.all((res :=array[t+1] - array[t])\
                          [~np.isnan(res)] >= 0.
                          )
                else unmet_case_values
                for t in range(records-1)])
           
    hour_TS_array = np.append(hour_TS_array,
                              np.mean(hour_TS_array[-2:], axis=0)[np.newaxis,:],
                              axis=0)