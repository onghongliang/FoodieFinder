import pandas as pd

def quick_sort_filter(data, col_name):
    if len(data) <= 1: #Base case: if the data has 0 or 1 row, it's already sorted
        return data
    else:
        pivot = data[col_name].iloc[len(data) // 2]
        left = data[data[col_name] < pivot] #column value is less than the pivot
        middle = data[data[col_name] == pivot] #column value is equal to the pivot
        right = data[data[col_name] > pivot] #column value is greater than the pivot
        
         # Recursively apply the quick sort algorithm to the left and right parts
        return pd.concat([quick_sort_filter(left, col_name), middle, quick_sort_filter(right, col_name)])
