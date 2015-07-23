import numpy as np
import sklearn.linear_model

from HPOlibConfigSpace.configuration_space import ConfigurationSpace
from HPOlibConfigSpace.hyperparameters import UniformFloatHyperparameter, \
    UnParametrizedHyperparameter

from ParamSklearn.components.base import ParamSklearnRegressionAlgorithm
from ParamSklearn.util import DENSE, SPARSE, PREDICTIONS


class RidgeRegression(ParamSklearnRegressionAlgorithm):
    def __init__(self, alpha, fit_intercept, tol, random_state=None):
        self.alpha = float(alpha)
        self.fit_intercept = fit_intercept == 'True'
        self.tol = float(tol)
        self.random_state = random_state
        self.estimator = None

    def fit(self, X, Y):
        self.estimator = sklearn.linear_model.Ridge(alpha=self.alpha,
                                                    fit_intercept=self.fit_intercept,
                                                    tol=self.tol,
                                                    copy_X=False,
                                                    normalize=False)
        self.estimator.fit(X, Y)
        return self

    def predict(self, X):
        if self.estimator is None:
            raise NotImplementedError
        return self.estimator.predict(X)

    @staticmethod
    def get_properties():
        return {'shortname': 'Rigde',
                'name': 'Ridge Regression',
                'handles_missing_values': False,
                'handles_nominal_values': False,
                'handles_numerical_features': True,
                'prefers_data_scaled': True,
                # TODO find out if this is good because of sparcity...
                'handles_regression': True,
                'handles_classification': False,
                'handles_multiclass': False,
                'handles_multilabel': False,
                'prefers_data_normalized': True,
                'is_deterministic': True,
                'handles_sparse': True,
                'input': (SPARSE, DENSE),
                'output': PREDICTIONS,
                # TODO find out what is best used here!
                # But rather fortran or C-contiguous?
                'preferred_dtype': np.float32}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties=None):
        cs = ConfigurationSpace()
        alpha = cs.add_hyperparameter(UniformFloatHyperparameter(
            "alpha", 10 ** -5, 10., log=True, default=1.))
        fit_intercept = cs.add_hyperparameter(UnParametrizedHyperparameter(
            "fit_intercept", "True"))
        tol = cs.add_hyperparameter(UniformFloatHyperparameter(
            "tol", 1e-5, 1e-1, default=1e-4, log=True))
        return cs

    def __str__(self):
        return "ParamSklearn Ridge Regression"
