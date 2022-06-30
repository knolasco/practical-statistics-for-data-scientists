import pandas as pd
import os
from scipy.stats import trim_mean
import numpy as np
import wquantiles
from statsmodels import robust

DATA_PATH = 'data'

# Different ways of measuring "center"
# simple ways to measure datasets using pandas and scipy.stats
state = pd.read_csv(os.path.join(DATA_PATH, 'state.csv'))
mean_ = state['Population'].mean()
trimmed_mean_ = trim_mean(state['Population'], 0.1)
median_ = state['Population'].median()

print('Mean : {:,.2f}'.format(mean_))
print('Trim Mean : {:,.2f}'.format(trimmed_mean_))
print('Median : {:,.2f}'.format(median_))
print('\n')

# using weighted mean through numpy
# finding average murder rate
w_mean = np.average(state['Murder.Rate'], weights = state['Population']) # weight lower populations higher?
# finding median murder rate as a weighted median (using wquantiles package)
w_median = wquantiles.median(state['Murder.Rate'], weights = state['Population'])

print('Weighted Mean : {:,.2f}%'.format(w_mean))
print('Weighted Median : {:,.2f}%'.format(w_median))
print('\n')

# Different ways of calculating the spread
# calculate std with pandas
stand_d = state['Population'].std()
# IQR (Range of values between 75th percentile and 25th percentile) 
IQR = state['Population'].quantile(0.75) - state['Population'].quantile(0.25)
# MAD using statsmodels
MAD = robust.scale.mad(state['Population'])
print('Standard Deviation : {:,.2f}'.format(stand_d))
print('IQR : {:,.2f}'.format(IQR))
print('MAD : {:,.2f}'.format(MAD))