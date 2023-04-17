# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 15:07:08 2023

@author: DE125135
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from ydata_profiling import ProfileReport

df_train = pd.read_csv("train.csv", low_memory=False)
df_test = pd.read_csv("test.csv")
df_store = pd.read_csv("store.csv")

print(df_train['DayOfWeek'].unique())
print(df_train['Open'].unique())
print(df_train['Promo'].unique())
print(df_train['StateHoliday'].unique())
print(df_train['SchoolHoliday'].unique())

print(df_train.columns)
print(df_train.shape)

print(df_store.columns)
print(df_store.shape)

#profile = ProfileReport(df_train, title="Pandas Profiling Report", explorative=True)
#profile.to_notebook_iframe()
#profile.to_file("train.html")

df_train_store = pd.merge(df_train, df_store, on="Store", how="inner")

#print(df_train_store.columns)

df_train_store.shape

#sns.heatmap(df_train_store.isnull())

# Welche StoreTypes sind besonders lukrativ
# Verschiedene Forecasts miteinander vergleichen
# Explorativ (auch für das "Vorstandsmeeting")