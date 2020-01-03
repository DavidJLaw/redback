import pandas as pd
from grb_bilby.processing import getdata
import os
dirname = os.path.dirname(__file__)
"""
Default save location is the data folder, but you can specify to be any folder you want
"""

def process_long_grbs(use_default_directory = False):
    data = pd.read_csv(dirname+'/LGRB_table.txt', header=0,
                       error_bad_lines=False, delimiter='\t', dtype='str')

    for GRB in data['GRB'].values:
        getdata.RetrieveAndProcessData(GRB,use_default_directory=use_default_directory)

    return print('Flux data for all long GRBs added')

def process_short_grbs(use_default_directory = False):
    data = pd.read_csv(dirname+'/SGRB_table.txt', header=0,
                       error_bad_lines=False, delimiter='\t', dtype='str')

    for GRB in data['GRB'].values:
        getdata.RetrieveAndProcessData(GRB,use_default_directory=use_default_directory)

    return print('Flux data for all short GRBs added')

def process_grbs_w_redshift(use_default_directory = False):
    data = pd.read_csv(dirname+'/GRBs_w_redshift.txt', header=0,
                       error_bad_lines=False, delimiter='\t', dtype='str')

    for GRB in data['GRB'].values:
        getdata.RetrieveAndProcessData(GRB, use_default_directory=use_default_directory)

    return print('Flux data for all GRBs with redshift added')

def process_grb_list(data, use_default_directory = False):
    """
    :param data: a list containing telephone number of GRB needing to processs
    :param type: whether GRB is a short or a long
    :param GRBdir: directory to save processed files to, 'default' for data folder and '.'
    for new local folder
    :return: saves the flux file in the location specified
    """

    for GRB in data:
        getdata.RetrieveAndProcessData(GRB, use_default_directory=use_default_directory)

    return print('Flux data for all GRBs in list added')
