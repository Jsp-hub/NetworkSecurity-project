from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

'''This NetworkModel class is the actual estimator of whether the site is phishing or not from the new provided data'''
'''also we will only provide the best model to this class for the future prediction'''
class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor                 # initialised KNNimputer
            self.model = model                               # initialised model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)      # this will fill out missing values using KNNimputer if the provided new data has missing features(data transformation ster)
            y_hat = self.model.predict(x_transform)           # prediction
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)