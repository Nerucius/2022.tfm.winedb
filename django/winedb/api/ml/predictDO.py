# CatBoost
from catboost import CatBoostClassifier
import numpy as np
from collections import OrderedDict
from operator import itemgetter


class multiple_CatBoostClassifier(CatBoostClassifier):
    
    def __init__(self,**args):
        super().__init__(**args)
    
    def predict_do(self,X):
        # X is an array of string and we need to convert into an ordered binary array
        ordered_list = np.zeros(len(self.feature_names_))
        i=0
        for feature in self.feature_names_:
            if feature in X: ordered_list[i] = 1
            i += 1

        
        #Predict Probabilities
        prediction_probabilities =  self.predict_proba(ordered_list)
        prediction_dic = dict(zip(self.classes_,prediction_probabilities))
        prediction_ordered_dic = OrderedDict(sorted(prediction_dic.items(), key=itemgetter(1),reverse=True))
        return prediction_ordered_dic
