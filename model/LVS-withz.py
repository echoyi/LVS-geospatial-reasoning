from pymc3 import Poisson, Uniform, Categorical, Normal, MvNormal
from pymc3 import *
import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import theano.tensor as tt

df_train = pd.read_csv('../data/synthetic/synthetic-3C2D.csv',index_col=0)
df_train=df_train.reset_index()
w_true = np.array([[1,-2,2],
                  [3,1,0],])
b_true = np.array([-1,5,2]).reshape((1,3))
x = df_train[['feature1', 'feature2']]
y_noisy = df_train['noisy target']


k=3
m= x.shape[1]
n= x.shape[0]
# num_classes = k
# num_features = m

with Model() as model:
    #assume five classes
    pi = pm.Dirichlet('pi',np.array([1]*k))
    z = Categorical(name='z',p=pi, shape=(n))
    w = Normal('w', mu=0, sd=1, shape=(m,k))
    b = Normal('b',mu=0,sd=1, shape=(1,k))
    σ  = pm.HalfCauchy('σ',0.2)
    
    w1 = pm.Deterministic('w1', w[:,z])
    b1 = pm.Deterministic('b1', tt.sort(b)[:,z])
    
    y = b1 + pm.math.dot(x,w1)
    
    #sd is noise in here
    # use log of price in the actual model
    price = pm.Normal('price', mu=y, sd=σ, observed=y_noisy)

with model:
    trace = pm.sample(20000, tune=10000)


pm.save_trace(trace,'withz.trace')