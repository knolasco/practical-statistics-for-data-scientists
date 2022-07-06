import pandas as pd
import os
from scipy.stats import trim_mean
import numpy as np
import wquantiles
from statsmodels import robust
import matplotlib.pyplot as plt

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

# percentiles with pandas
print('\n')
print(state['Murder.Rate'].quantile([0.05, 0.25, 0.5, 0.75, 0.95]))

# using pandas to create a boxplot
ax = (state['Population']/1_000_000).plot.box()
ax.set_ylabel('Population (millions)')
# need to call plt to show the graph
plt.tight_layout()
plt.show()

# frequencies and histograms
# use pandas.cut() with value_counts to bin continuous data
print('\n')
binned_population = pd.cut(state['Population'], bins = 10)
print(binned_population.value_counts())

# code to create table 1.5
binned_population.name = 'binnedPopulation'
df = pd.concat([state, binned_population], axis = 1) # add columns to states df
df = df.sort_values(by = 'Population')

# use group by for the for loop
groups = []
for group, subset in df.groupby(by = 'binnedPopulation'):
    groups.append({
        'BinRange' : group,
        'Count' : len(subset),
        'States' : ', '.join(subset['Abbreviation'])
    })
print('\n', pd.DataFrame(groups))

# plot a histogram with pandas
ax = (state['Population'] / 100_000_000).plot.hist(figsize = (4,4))
ax.set_xlabel('Population(millions)')
plt.tight_layout()
plt.show()