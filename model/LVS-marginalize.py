import theano.tensor as tt
import theano
import pymc3 as pm
from pymc3 import *
from pymc3 import Poisson, Uniform, Categorical, Normal, MvNormal
import numpy as np
import pandas as pd

w_true = np.array([[1,-2,2],
                  [3,1,0],])
b_true = np.array([-1,5,2]).reshape((1,3))

df_train = pd.read_csv('../data/synthetic/synthetic-3C2D.csv',index_col=0)
df_train = df_train.reset_index()
x = df_train[['feature1', 'feature2']]
y_noisy = df_train['noisy target']

k=3
m= x.shape[1]
n= x.shape[0]
# num_classes = k
# num_features = m

with Model() as marginalizedModel:
    pi = pm.Dirichlet('pi',np.array([1]*k))

    #regression parameter
    w = Normal('w', mu=0, sd=1, shape=(m,k))
    b = Normal('b',mu=0,sd=1, shape=(1,k))
    σ  = pm.HalfCauchy('σ',0.2, shape=k)
    
    y = b+pm.math.dot(x,w)
    
    #sd is noise in here
    # use log of price in the actual model
    price = pm.NormalMixture('price', pi, mu=y, sigma=σ, observed=y_noisy)

#fit model
with marginalizedModel:
    trace = pm.sample(100, tune=10)


pm.save_trace(trace,'marginalize.trace')