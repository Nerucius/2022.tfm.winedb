import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def create_variety_synonyms_dictonary(varieity_map_path):
    """
    Return an variety map from variety synomis Excel structed in columns for example:
    garnacha | macabeo
    lledoner | viura
             | macabeu

    """
    # Create the varieity_map from variety path
    df_unique_varieities = pd.read_excel(varieity_map_path)

    varieity_map={}
    for varieity in df_unique_varieities.columns:
        for other_variety_name in df_unique_varieities[varieity].unique():
            if other_variety_name!=np.nan:
                varieity_map[other_variety_name] = varieity
    
    return varieity_map

def clean_variety(variety, variety_map, min_per=20):
    
    # extracting the percentage 
    pattern = r"(\d*\.?\d+%)"
    percentage = re.findall(pattern, variety)
    
    # Handle the case where only a percentage is given but not the variety
    if re.sub(pattern, '', variety) == "":
        return None  
    
    # Filter by minimum percentage
    if len(percentage) > 0 and float(percentage[0][:-1]) < min_per:
        return None
    
    # cleaning and saving the variety
    variety_cleaned = re.sub(pattern+" ", '', variety)
    
    #Check if there are synonyms
    if variety_cleaned in variety_map.keys():
        return variety_map[variety_cleaned]
    else:
        return variety_cleaned

def barplot_wine_aspect(series, title='Count of aspect', thres=80,save_excel=False,plot=False,orient="h"):

    counter = defaultdict(lambda: 0)

    def add_to_counter(arr):   
        try:
            for i in arr:
                counter[i] += 1
        except Exception:
            pass

    series.map(add_to_counter)

    # Construct dataframe and sort descending
    counter = pd.DataFrame(index=counter.keys(), data=counter.values(), columns=['count'])
    counter = counter.sort_values(by="count",ascending=False).reset_index()

    if save_excel: counter.to_excel("dict.xlsx")
    
    # Calcualte percent of each aspect and cumsum column
    counter['percent'] = (counter['count'] / counter['count'].sum()) * 100
    counter['percent_cumsum'] = counter.percent.cumsum()

    # save the original number of different attributes
    n_start = len(counter)

    # Filter by threshold, use '100' to disable
    counter = counter[counter['percent_cumsum'] <= thres]

    if plot:
        plt.figure(figsize=(16,5),dpi=130)

        if orient=="h":
            g = sns.barplot(data=counter, 
                            x="count",
                            y="index");
        if orient=="v":
            g = sns.barplot(data=counter, 
                y="count",
                x="index")
            plt.xticks(rotation = 90);
            #g.set_yscale("log")

        plt.title(title)
    
    # save the list of reduced attributes
    n_end = len(counter)
    
    return n_start,n_end,counter['index'].values

def create_onehot_encoding(df, series, feat_list):
    
    for feat_itm in feat_list:
        
        # helper
        def has_value(arr, itm):
            try:
                if isinstance(arr, list):
                    return int(itm in arr)
                else:
                    return int(itm == arr)
            except Exception:
                return 0
        if feat_itm in df.columns:
            df[feat_itm] =  np.maximum(df[feat_itm].values,series.apply(lambda x: has_value(x, feat_itm)))
        else:
            df[feat_itm] = series.apply(lambda x: has_value(x, feat_itm))