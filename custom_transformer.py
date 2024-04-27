import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class CustomSamplingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, age_threshold=51, value_threshold=500000, sample_size=100, random_state=200):
        self.age_threshold = age_threshold
        self.value_threshold = value_threshold
        self.sample_size = sample_size
        self.random_state = random_state

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        condition_age = X['housing_median_age'] > self.age_threshold
        condition_value = X['median_house_value'] > self.value_threshold
        sample_age = min(sum(condition_age), self.sample_size)
        sample_value = min(sum(condition_value), self.sample_size)

        sample_age_over_threshold = X[condition_age].sample(n=sample_age, random_state=self.random_state)
        sample_value_over_threshold = X[condition_value].sample(n=sample_value, random_state=self.random_state)
        filtered_data = X[~(condition_value | condition_age)]

        result_data = pd.concat([filtered_data, sample_age_over_threshold, sample_value_over_threshold])
        return result_data

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, drop_originals=True):
        self.drop_originals = drop_originals

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        # Création de nouvelles caractéristiques
        X['rooms_per_household'] = X['total_rooms'] / X['households']
        X['bedrooms_per_room'] = X['total_bedrooms'] / X['total_rooms']

        if self.drop_originals:
            X = X.drop(['total_rooms', 'total_bedrooms'], axis=1)

        return X
