import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
import plotly.express as px

fileName = 'retail_sales_dataset.csv'

class data_analizator:
    def __init__(self, fileName = fileName):
        self.data_frame = pd.read_csv(fileName)
        self.explore_columns = {self.data_frame.columns[i]:n.name 
                                for i, n in enumerate(self.data_frame.dtypes)}
    
    def review_columns(self):
        #convert column date to dataframe
        for i in self.explore_columns:
            if 'date' in i.lower() and self.explore_columns[i] == 'O':
                self.data_frame[i] = pd.to_datetime(self.data_frame[i])
        #fill na values
        for i in self.explore_columns:
            if self.explore_columns[i] == 'O':
                self.data_frame[i].fillna('N/A')
            elif self.explore_columns[i] == 'float64':
                self.data_frame[i].fillna(0.0)
            elif self.explore_columns[i] == 'int64':
                self.data_frame[i].fillna(0)
    
    def made_column_of_intervals(self, column_name = 'Age', n_intervals = 4):
        min_value = self.data_frame[column_name].min()
        max_value = self.data_frame[column_name].max()
        interval_value = int((max_value - min_value)/n_intervals)
        interval_values = []
        cut_value = min_value
        for i in range(4):
            interval_values.append(f'{cut_value} - {cut_value + interval_value}')
            cut_value += interval_value
        if int(interval_values[-1].split(' - ')[-1]) <= max_value:
            interval_values[-1] = interval_values[-1].split(' - ')[0] + ' - ' + str(max_value + 1)
        list_bins = [int(i.split(' - ')[0]) for i in interval_values]
        list_bins.append(int(interval_values[-1].split(' - ')[-1]))
        self.data_frame['Interval '+column_name] = pd.cut(self.data_frame[column_name], 
                                            bins=list_bins, 
                                            labels=interval_values,
                                            right=False)

    def gettotals_bygroupcolumn(self, columns, value_name, filter_column = None, filter_value = None):
        if type(filter_column) is None:
            table = self.data_frame
        else:
            table = self.data_frame[self.data_frame[filter_column] == filter_value]
        table_resume = table.groupby(columns)[value_name].sum()
        return table_resume
    
    def graph_relation_between_columns(self, column_x, column_y, filter_column = None, filter_value = None):
        if type(filter_column) is None:
            table = self.data_frame
        else:
            table = self.data_frame[self.data_frame[filter_column] == filter_value]
        fig = px.box(table, x=column_x, y=column_y, points='all')
        fig.show()

    def apply_ANOVA_test(self, column_name, value_name):
        groups_column = [
            self.data_frame[self.data_frame[column_name] == group][value_name] for group in self.data_frame[column_name].unique()
        ]
        r=stats.f_oneway(*groups_column)
    
