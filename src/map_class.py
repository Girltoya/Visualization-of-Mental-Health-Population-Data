import folium
import pandas as pd
import json
import geopandas as gpd
import os
import math
from pathlib import Path
import global_variables
from data import *
import numpy as np
import time

# symbolic constant to distinguish between normal maps and maps that represent growth
MAP_NORMAL_VER = 0
MAP_INCREASE_VER = 1
# symbolic constant to distinguish between CCG CODE and CCG NAME
COMMON_CCG_CODE = 0
COMMON_CCG_NAME = 1


def common_ccg_get(ver, diagnosis):
    """
    get common ccg
    :param ver: COMMON_CCG_CODE-get common ccg code, COMMON_CCG_NAME-get common ccg name
    :param diagnosis: symbolic constant of health diagnosis
    :return: common ccg code/name
    """
    ans = []
    col = ''
    # if health diagnosis is IAPT
    if diagnosis == DATASET_DIAGNOSIS_IAPT:
        # get the relevant column of ccg code/name
        if ver == COMMON_CCG_NAME:
            col = 'CCGName'
        elif ver == COMMON_CCG_CODE:
            col = 'CCG'
        # get global dataset group for health diagnosis-IAPT
        dataset = global_variables.get_value(global_variables.KEY_DATASET_IAPT)
        # get ccg code/name of each year (2019, 2020, 2021)
        ccg19 = np.array(dataset[0][0].dataset[col])
        ccg19 = ccg19.tolist()
        ccg20 = np.array(dataset[1][0].dataset[col])
        ccg20 = ccg20.tolist()
        ccg21 = np.array(dataset[2][0].dataset[col])
        ccg21 = ccg21.tolist()
        # get common ccg code/name list
        ans = list(set(ccg19) & set(ccg20))
        ans = list(set(ans) & set(ccg21))
    # if health diagnosis is CYPED
    elif diagnosis == DATASET_DIAGNOSIS_CYPED:
        # get global dataset group for health diagnosis-CYPED
        dataset = global_variables.get_value(global_variables.KEY_DATASET_CYPED)
        # get ccg code/name of each year (2019, 2020, 2021)
        ccg19 = np.array(dataset[0][0].dataset['CCG Code'])
        ccg19 = ccg19.tolist()
        ccg20 = np.array(dataset[1][0].dataset['CCG Code'])
        ccg20 = ccg20.tolist()
        ccg21 = np.array(dataset[2][0].dataset['CCG Code'])
        ccg21 = ccg21.tolist()
        # get common ccg code/name list
        ans1 = list(set(ccg19) & set(ccg20))
        ans1 = list(set(ans1) & set(ccg21))
        if ver == COMMON_CCG_CODE:
            ans = ans1
        elif ver == COMMON_CCG_NAME:
            for index, row in dataset[0][0].dataset.iterrows():
                if row['CCG Code'] in ans1:
                    ans.append(row['CCG Name'])
    # if health diagnosis is PHSMI
    elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
        # get the relevant column of ccg code/name
        if ver == COMMON_CCG_NAME:
            col = 'CCG Name'
        elif ver == COMMON_CCG_CODE:
            col = 'CCG Code'
        # get global dataset group for health diagnosis-PHSMI
        dataset = global_variables.get_value(global_variables.KEY_DATASET_PHSMI)
        # get ccg code/name of each year (2019, 2020, 2021)
        ccg19 = np.array(dataset[0][0].dataset[col])
        ccg19 = ccg19.tolist()
        ccg20 = np.array(dataset[1][0].dataset[col])
        ccg20 = ccg20.tolist()
        ccg21 = np.array(dataset[2][0].dataset[col])
        ccg21 = ccg21.tolist()
        # get common ccg code/name list
        ans = list(set(ccg19) & set(ccg20))
        ans = list(set(ans) & set(ccg21))
    # if health diagnosis is OAPS
    elif diagnosis == DATASET_DIAGNOSIS_OAPS:
        # get the relevant column of ccg code/name
        if ver == COMMON_CCG_NAME:
            col = 'Breakdown One Description'
        elif ver == COMMON_CCG_CODE:
            col = 'Breakdown One Code'
        # get global dataset group for health diagnosis-OAPS
        dataset = global_variables.get_value(global_variables.KEY_DATASET_OAPS)
        # get ccg code/name of each year (2019, 2020, 2021)
        ccg19 = np.array(dataset[0][0].dataset[col])
        ccg19 = ccg19.tolist()
        ccg20 = np.array(dataset[1][0].dataset[col])
        ccg20 = ccg20.tolist()
        ccg21 = np.array(dataset[2][0].dataset[col])
        ccg21 = ccg21.tolist()
        # get common ccg code/name list
        ans = list(set(ccg19) & set(ccg20))
        ans = list(set(ans) & set(ccg21))
    # remove the ccg that is ''
    for i in ans:
        if i == '':
            ans.remove(i)
    return ans


class NHSMentalHealthCCGMap:
    """
    Class for the Map of NHS Mental Health Population Data at CCG level
    """
    def __init__(self, map_name='mental_health_map'):
        """
        init parameters and load source data for data mapping from local disks
        :param map_name: default('mental_health_map')
        """
        # list of symbolic string to identify health diagnosis
        self.dataset_type_list = [DATASET_DIAGNOSIS_IAPT_STR, DATASET_DIAGNOSIS_CYPED_STR,
                                  DATASET_DIAGNOSIS_PHSMI_STR, DATASET_DIAGNOSIS_OAPS_STR]
        # local file path to store source data files
        self.data_path = os.path.join(os.path.dirname(os.getcwd()), "data/")
        # local file path to store new files generated during the visualization process
        self.new_file_path = os.path.join(os.path.dirname(os.getcwd()), "newfile/")
        # list of local file paths for geospatial files (geojson file)
        self.geo_file_path = []
        # list of geospatial data (geopandas data read from geojson file)
        self.geo_data = []
        # list of ccg names and codes files
        self.ccg_code_data = []

        # init local file path for geospatial files
        geo_path = self.data_path + GEO_JASON_FILE_DIR
        path = geo_path + GEO_JASON_FILE_NAME_2019
        self.geo_file_path.append(path)
        path = geo_path + GEO_JASON_FILE_NAME_2020
        self.geo_file_path.append(path)
        path = geo_path + GEO_JASON_FILE_NAME_2021
        self.geo_file_path.append(path)
        # read geo jason file
        data = gpd.read_file(geo_path + GEO_JASON_FILE_NAME_2019)
        self.geo_data.append(data)
        data = gpd.read_file(geo_path + GEO_JASON_FILE_NAME_2020)
        self.geo_data.append(data)
        data = gpd.read_file(geo_path + GEO_JASON_FILE_NAME_2021)
        self.geo_data.append(data)
        # read ccg names and codes file
        data = pd.read_csv(geo_path + CCG_NAMES_AND_CODES_FILE_NAME_2019)
        self.ccg_code_data.append(data)
        data = pd.read_csv(geo_path + CCG_NAMES_AND_CODES_FILE_NAME_2020)
        self.ccg_code_data.append(data)
        data = pd.read_csv(geo_path + CCG_NAMES_AND_CODES_FILE_NAME_2021)
        self.ccg_code_data.append(data)
        # save data of ccg names and codes file as global variable
        global_variables.set_value(global_variables.KEY_CCG_CODE, self.ccg_code_data)
        # read dataset
        # read iapt dataset
        iapt_path = self.data_path + DATASET_IAPT_FILE_DIR
        dataset_info_iapt2019_q1 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2019_20_QUARTER1,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER1)
        self.dataset_info_iapt = [[dataset_info_iapt2019_q1] * 4 for _ in range(3)]
        self.dataset_info_iapt[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1] = dataset_info_iapt2019_q1
        dataset_info_iapt2019_q2 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2019_20_QUARTER2,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER2)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER2] = dataset_info_iapt2019_q2
        dataset_info_iapt2019_q3 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2019_20_QUARTER3,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER3)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER3] = dataset_info_iapt2019_q3
        dataset_info_iapt2019_q4 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2019_20_QUARTER4,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER4)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER4] = dataset_info_iapt2019_q4
        dataset_info_iapt2020_q1 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2020_21_QUARTER1,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2020_21, DATASET_TIME_QUARTER1)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER1] = dataset_info_iapt2020_q1
        dataset_info_iapt2020_q2 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2020_21_QUARTER2,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2020_21, DATASET_TIME_QUARTER2)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER2] = dataset_info_iapt2020_q2
        dataset_info_iapt2020_q3 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2020_21_QUARTER3,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2020_21, DATASET_TIME_QUARTER3)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER3] = dataset_info_iapt2020_q3
        dataset_info_iapt2020_q4 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2020_21_QUARTER4,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2020_21, DATASET_TIME_QUARTER4)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER4] = dataset_info_iapt2020_q4
        dataset_info_iapt2021_q1 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2021_22_QUARTER1,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2021_22, DATASET_TIME_QUARTER1)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER1] = dataset_info_iapt2021_q1
        dataset_info_iapt2021_q2 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2021_22_QUARTER2,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2021_22, DATASET_TIME_QUARTER2)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER2] = dataset_info_iapt2021_q2
        dataset_info_iapt2021_q3 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2021_22_QUARTER3,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2021_22, DATASET_TIME_QUARTER3)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER3] = dataset_info_iapt2021_q3
        dataset_info_iapt2021_q4 = DatasetInfo(iapt_path + DATASET_IAPT_FILE_NAME_2021_22_QUARTER4,
                                               DATASET_DIAGNOSIS_IAPT,
                                               DATASET_TIME_YEAR_2021_22, DATASET_TIME_QUARTER4)
        self.dataset_info_iapt[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER4] = dataset_info_iapt2021_q4

        # read CYPED dataset
        cyped_path = self.data_path + DATASET_CYPED_FILE_DIR
        dataset_info_cyped2019_q1 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2019_20_QUARTER1,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER1)
        self.dataset_info_cyped = [[dataset_info_cyped2019_q1] * 4 for _ in range(3)]
        self.dataset_info_cyped[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1] = dataset_info_cyped2019_q1
        dataset_info_cyped2019_q2 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2019_20_QUARTER2,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER2)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER2] = dataset_info_cyped2019_q2
        dataset_info_cyped2019_q3 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2019_20_QUARTER3,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER3)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER3] = dataset_info_cyped2019_q3
        dataset_info_cyped2019_q4 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2019_20_QUARTER4,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER4)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER4] = dataset_info_cyped2019_q4
        dataset_info_cyped2020_q1 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2020_21_QUARTER1,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER1)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER1] = dataset_info_cyped2020_q1
        dataset_info_cyped2020_q2 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2020_21_QUARTER2,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER2)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER2] = dataset_info_cyped2020_q2
        dataset_info_cyped2020_q3 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2020_21_QUARTER3,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER3)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER3] = dataset_info_cyped2020_q3
        dataset_info_cyped2020_q4 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2020_21_QUARTER4,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER4)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER4] = dataset_info_cyped2020_q4
        dataset_info_cyped2021_q1 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2021_22_QUARTER1,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER1)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER1] = dataset_info_cyped2021_q1
        dataset_info_cyped2021_q2 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2021_22_QUARTER2,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER2)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER2] = dataset_info_cyped2021_q2
        dataset_info_cyped2021_q3 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2021_22_QUARTER3,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER3)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER3] = dataset_info_cyped2021_q3
        dataset_info_cyped2021_q4 = DatasetInfo(cyped_path + DATASET_CYPED_FILE_NAME_2021_22_QUARTER4,
                                                DATASET_DIAGNOSIS_CYPED, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER4)
        self.dataset_info_cyped[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER4] = dataset_info_cyped2021_q4

        # read phsmi dataset
        phsmi_path = self.data_path + DATASET_PHSMI_FILE_DIR
        dataset_info_phsmi2019_q1 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2019_20_QUARTER1,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER1)
        self.dataset_info_phsmi = [[dataset_info_phsmi2019_q1] * 4 for _ in range(3)]
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1] = dataset_info_phsmi2019_q1
        dataset_info_phsmi2019_q2 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2019_20_QUARTER2,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER2)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER2] = dataset_info_phsmi2019_q2
        dataset_info_phsmi2019_q3 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2019_20_QUARTER3,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER3)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER3] = dataset_info_phsmi2019_q3
        dataset_info_phsmi2019_q4 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2019_20_QUARTER4,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2019_20,
                                                DATASET_TIME_QUARTER4)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER4] = dataset_info_phsmi2019_q4
        dataset_info_phsmi2020_q1 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2020_21_QUARTER1,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER1)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER1] = dataset_info_phsmi2020_q1
        dataset_info_phsmi2020_q2 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2020_21_QUARTER2,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER2)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER2] = dataset_info_phsmi2020_q2
        dataset_info_phsmi2020_q3 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2020_21_QUARTER3,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER3)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER3] = dataset_info_phsmi2020_q3
        dataset_info_phsmi2020_q4 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2020_21_QUARTER4,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2020_21,
                                                DATASET_TIME_QUARTER4)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER4] = dataset_info_phsmi2020_q4
        dataset_info_phsmi2021_q1 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2021_22_QUARTER1,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER1)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER1] = dataset_info_phsmi2021_q1
        dataset_info_phsmi2021_q2 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2021_22_QUARTER2,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER2)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER2] = dataset_info_phsmi2021_q2
        dataset_info_phsmi2021_q3 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2021_22_QUARTER3,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER3)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER3] = dataset_info_phsmi2021_q3
        dataset_info_phsmi2021_q4 = DatasetInfo(phsmi_path + DATASET_PHSMI_FILE_NAME_2021_22_QUARTER4,
                                                DATASET_DIAGNOSIS_PHSMI, DATASET_TIME_YEAR_2021_22,
                                                DATASET_TIME_QUARTER4)
        self.dataset_info_phsmi[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER4] = dataset_info_phsmi2021_q4

        # read oaps dataset
        start_time = time.time()
        oaps_path = self.data_path + DATASET_OAPS_FILE_DIR
        dataset_info_oaps2019_q1 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2019_20_QUARTER1,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2019_20,
                                               DATASET_TIME_QUARTER1)
        self.dataset_info_oaps = [[dataset_info_oaps2019_q1] * 4 for _ in range(3)]
        self.dataset_info_oaps[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1] = dataset_info_oaps2019_q1
        dataset_info_oaps2019_q2 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2019_20_QUARTER2,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2019_20,
                                               DATASET_TIME_QUARTER2)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER2] = dataset_info_oaps2019_q2
        dataset_info_oaps2019_q3 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2019_20_QUARTER3,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2019_20,
                                               DATASET_TIME_QUARTER3)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER3] = dataset_info_oaps2019_q3
        dataset_info_oaps2019_q4 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2019_20_QUARTER4,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2019_20,
                                               DATASET_TIME_QUARTER4)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER4] = dataset_info_oaps2019_q4
        dataset_info_oaps2020_q1 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2020_21_QUARTER1,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2020_21,
                                               DATASET_TIME_QUARTER1)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER1] = dataset_info_oaps2020_q1
        dataset_info_oaps2020_q2 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2020_21_QUARTER2,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2020_21,
                                               DATASET_TIME_QUARTER2)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER2] = dataset_info_oaps2020_q2
        dataset_info_oaps2020_q3 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2020_21_QUARTER3,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2020_21,
                                               DATASET_TIME_QUARTER3)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER3] = dataset_info_oaps2020_q3
        dataset_info_oaps2020_q4 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2020_21_QUARTER4,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2020_21,
                                               DATASET_TIME_QUARTER4)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2020_21][DATASET_TIME_QUARTER4] = dataset_info_oaps2020_q4
        dataset_info_oaps2021_q1 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2021_22_QUARTER1,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2021_22,
                                               DATASET_TIME_QUARTER1)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER1] = dataset_info_oaps2021_q1
        dataset_info_oaps2021_q2 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2021_22_QUARTER2,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2021_22,
                                               DATASET_TIME_QUARTER2)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER2] = dataset_info_oaps2021_q2
        dataset_info_oaps2021_q3 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2021_22_QUARTER3,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2021_22,
                                               DATASET_TIME_QUARTER3)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER3] = dataset_info_oaps2021_q3
        dataset_info_oaps2021_q4 = DatasetInfo(oaps_path + DATASET_OAPS_FILE_NAME_2021_22_QUARTER4,
                                               DATASET_DIAGNOSIS_OAPS, DATASET_TIME_YEAR_2021_22,
                                               DATASET_TIME_QUARTER4)
        self.dataset_info_oaps[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER4] = dataset_info_oaps2021_q4

        # do data preprocessing
        self.data_preprocessing()
        # save datasets for all health diagnoses as global variables
        global_variables.set_value(global_variables.KEY_DATASET_IAPT, self.dataset_info_iapt)
        global_variables.set_value(global_variables.KEY_DATASET_CYPED, self.dataset_info_cyped)
        global_variables.set_value(global_variables.KEY_DATASET_PHSMI, self.dataset_info_phsmi)
        global_variables.set_value(global_variables.KEY_DATASET_OAPS, self.dataset_info_oaps)

    def data_preprocessing(self):
        """
        pre-process data read from local disks
        1. assigns the value of all special symbols in the table to 0
        2. change all data in the table to values formatted as string to float type
        :return: none
        """
        # dataset for each year
        for year in range(3):
            # dataset for each quarter
            for quarter in range(4):
                # data processing for iapt
                shape = self.dataset_info_iapt[year][quarter].dataset.shape
                # data for each row
                for i in range(shape[0]):
                    # data for each column
                    # assigns the value of all special symbols in the table to '0'
                    for j in range(DATASET_IAPT_VARIABLE_FIELD_INDEX_START, shape[1]):
                        if self.dataset_info_iapt[year][quarter].dataset.iloc[i, j] == '*' \
                                or self.dataset_info_iapt[year][quarter].dataset.iloc[i, j] == '-':
                            self.dataset_info_iapt[year][quarter].dataset.iloc[i, j] = '0'
                        elif math.isnan(float(self.dataset_info_iapt[year][quarter].dataset.iloc[i, j])):
                            self.dataset_info_iapt[year][quarter].dataset.iloc[i, j] = '0'
                # same data processing for cyped
                shape = self.dataset_info_cyped[year][quarter].dataset.shape
                for i in range(shape[0]):
                    for j in range(DATASET_CYPED_VARIABLE_FIELD_INDEX_START, shape[1]):
                        if self.dataset_info_cyped[year][quarter].dataset.iloc[i, j] == '*' \
                                or self.dataset_info_cyped[year][quarter].dataset.iloc[i, j] == '-'\
                                or self.dataset_info_cyped[year][quarter].dataset.iloc[i, j] == '':
                            self.dataset_info_cyped[year][quarter].dataset.iloc[i, j] = '0'
                        elif math.isnan(float(self.dataset_info_cyped[year][quarter].dataset.iloc[i, j])):
                            self.dataset_info_cyped[year][quarter].dataset.iloc[i, j] = '0'
                # same data processing for phsmi
                shape = self.dataset_info_phsmi[year][quarter].dataset.shape
                for i in range(shape[0]):
                    for j in range(DATASET_PHSMI_VARIABLE_FIELD_INDEX_START, shape[1]):
                        if self.dataset_info_phsmi[year][quarter].dataset.iloc[i, j] == '*' \
                                or self.dataset_info_phsmi[year][quarter].dataset.iloc[i, j] == '-':
                            self.dataset_info_phsmi[year][quarter].dataset.iloc[i, j] = '0'
                        elif math.isnan(float(self.dataset_info_phsmi[year][quarter].dataset.iloc[i, j])):
                            self.dataset_info_phsmi[year][quarter].dataset.iloc[i, j] = '0'
                # same data processing for oaps
                shape = self.dataset_info_oaps[year][quarter].dataset.shape
                for i in range(shape[0]):
                    for j in range(DATASET_OAPS_VARIABLE_FIELD_INDEX_START, shape[1]):
                        if self.dataset_info_oaps[year][quarter].dataset.iloc[i, j] == '*' \
                                or self.dataset_info_oaps[year][quarter].dataset.iloc[i, j] == '-'\
                                or self.dataset_info_oaps[year][quarter].dataset.iloc[i, j] == '':
                            self.dataset_info_oaps[year][quarter].dataset.iloc[i, j] = '0'
                        elif math.isnan(float(self.dataset_info_oaps[year][quarter].dataset.iloc[i, j])):
                            self.dataset_info_oaps[year][quarter].dataset.iloc[i, j] = '0'
        # dataset for each year
        for year in range(3):
            # dataset for each quarter
            for quarter in range(4):
                # data processing for iapt
                # change all data in the table to values formatted as string to float type
                for var_name in self.dataset_info_iapt[year][quarter].variable_list:
                    self.dataset_info_iapt[year][quarter].dataset[var_name] = \
                        self.dataset_info_iapt[year][quarter].dataset[var_name].astype('float')
                # same data processing for cyped
                for var_name in self.dataset_info_cyped[year][quarter].variable_list:
                    self.dataset_info_cyped[year][quarter].dataset[var_name] = \
                        self.dataset_info_cyped[year][quarter].dataset[var_name].astype('float')
                # same data processing for phsmi
                for var_name in self.dataset_info_phsmi[year][quarter].variable_list:
                    self.dataset_info_phsmi[year][quarter].dataset[var_name] = \
                        self.dataset_info_phsmi[year][quarter].dataset[var_name].astype('float')
                # same data processing for oaps
                for var_name in self.dataset_info_oaps[year][quarter].variable_list:
                    self.dataset_info_oaps[year][quarter].dataset[var_name] = \
                        self.dataset_info_oaps[year][quarter].dataset[var_name].astype('float')

    def choropleth_map_new_geofile_name_get(self, version, diagnosis, year, quarter, var):
        """
        get new geospatial file (generated during visualization) name for choropleth map
        (for different health diagnosis, year, quarter, and variables)
        :param version: MAP_NORMAL_VER-normal maps, MAP_INCREASE_VER-maps that represent growth
        :param diagnosis: symbolic constant to identify health diagnosis
        :param year: symbolic constant to identify different year
        :param quarter: symbolic constant to identify different quarter
        :param var: variable name
        :return: file name
        """
        file_name = ''
        name_str = ''
        # add additional string to identify map version
        if version == MAP_INCREASE_VER:
            name_str = '_increase'
        # create geojson file name for different health diagnosis, year, quarter, and variables
        if diagnosis == DATASET_DIAGNOSIS_IAPT:
            file_name = self.new_file_path + 'iapt_geofile' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.geojson'
        elif diagnosis == DATASET_DIAGNOSIS_CYPED:
            file_name = self.new_file_path + 'cyped_geofile' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.geojson'
        elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
            file_name = self.new_file_path + 'phsmi_geofile' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.geojson'
        elif diagnosis == DATASET_DIAGNOSIS_OAPS:
            file_name = self.new_file_path + 'oaps_geofile' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.geojson'
        return file_name

    def CCG_CD_convert2FID(self, df, code, cd_col):
        """
        get value of column 'FID' according to the code
        :param df: data frame
        :param code: value of input column name
        :param cd_col: column name
        :return:
        """
        for index, row in df.iterrows():
            if row[cd_col] == code:
                return row['FID']
        return -1

    def CCG_FID_get_var(self, df, fid, var_name):
        """
        get the value of column "var_name" according to fid
        :param df: dataframe
        :param fid: value of column "FID"
        :param var_name: variable name
        :return: value of column "var_name"
        """
        for index, row in df.iterrows():
            if row['FID'] == fid:
                if math.isnan(row[var_name]):
                    return 0
                else:
                    return int(row[var_name])
        return 0

    def create_new_geojson(self, version, type, year, quarter, var, mapped_data):
        """
        create a new geojson file: add mental health data into original geospatial file (geojson file)
        :param version: MAP_NORMAL_VER-normal maps, MAP_INCREASE_VER-maps that represent growth
        :param type: symbolic constant to identify health diagnosis
        :param year: symbolic constant to identify different year
        :param quarter: symbolic constant to identify different quarter
        :param var: variable name
        :param mapped_data: mental health data which should be mapped to the geographic map
        :return: none
        """
        # open original geospatial file (geojson file)
        with open(self.geo_file_path[year], 'r') as j:
            geo_data = json.loads(j.read())
        # get code and names file data
        code_data = self.ccg_code_data[year]
        # add mental health data - IAPT into original geospatial file
        if type == DATASET_DIAGNOSIS_IAPT:
            # for each feature
            for features in geo_data['features']:
                fid = -1
                # get fid according to CCG code
                # the dataset of different year has different column names for the same variable
                if year == DATASET_TIME_YEAR_2019_20:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG19CD'], 'CCG19CD')
                elif year == DATASET_TIME_YEAR_2020_21:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['ccg20cd'], 'CCG20CD')
                elif year == DATASET_TIME_YEAR_2021_22:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG21CD'], 'CCG21CD')
                # write fid into geojson file
                features['properties'].update({'FID': fid})
                # if it is normal map, add all the variables value into geojson file
                if version == MAP_NORMAL_VER:
                    for var_name in self.dataset_info_iapt[year][quarter].variable_list:
                        features['properties'].update({var_name: self.CCG_FID_get_var(mapped_data, fid, var_name)})
                # if it is increasing map, just add increase value into geojson file
                elif version == MAP_INCREASE_VER:
                    features['properties'].update({'increase': self.CCG_FID_get_var(mapped_data, fid, 'increase')})
        # add mental health data - CYPED into original geospatial file
        elif type == DATASET_DIAGNOSIS_CYPED:
            for features in geo_data['features']:
                fid = -1
                if year == DATASET_TIME_YEAR_2019_20:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG19CD'], 'CCG19CD')
                elif year == DATASET_TIME_YEAR_2020_21:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['ccg20cd'], 'CCG20CD')
                elif year == DATASET_TIME_YEAR_2021_22:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG21CD'], 'CCG21CD')
                features['properties'].update({'FID': fid})
                if version == MAP_NORMAL_VER:
                    for var_name in self.dataset_info_cyped[year][quarter].variable_list:
                        features['properties'].update({var_name: self.CCG_FID_get_var(mapped_data, fid, var_name)})
                elif version == MAP_INCREASE_VER:
                    features['properties'].update({'increase': self.CCG_FID_get_var(mapped_data, fid, 'increase')})
        # add mental health data - PHSMI into original geospatial file
        elif type == DATASET_DIAGNOSIS_PHSMI:
            for features in geo_data['features']:
                fid = -1
                if year == DATASET_TIME_YEAR_2019_20:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG19CD'], 'CCG19CD')
                elif year == DATASET_TIME_YEAR_2020_21:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['ccg20cd'], 'CCG20CD')
                elif year == DATASET_TIME_YEAR_2021_22:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG21CD'], 'CCG21CD')
                features['properties'].update({'FID': fid})
                if version == MAP_NORMAL_VER:
                    for var_name in self.dataset_info_phsmi[year][quarter].variable_list:
                        features['properties'].update({var_name: self.CCG_FID_get_var(mapped_data, fid, var_name)})
                elif version == MAP_INCREASE_VER:
                    features['properties'].update({'increase': self.CCG_FID_get_var(mapped_data, fid, 'increase')})
        # add mental health data - OAPS into original geospatial file
        elif type == DATASET_DIAGNOSIS_OAPS:
            for features in geo_data['features']:
                fid = -1
                if year == DATASET_TIME_YEAR_2019_20:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG19CD'], 'CCG19CD')
                elif year == DATASET_TIME_YEAR_2020_21:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['ccg20cd'], 'CCG20CD')
                elif year == DATASET_TIME_YEAR_2021_22:
                    fid = self.CCG_CD_convert2FID(code_data, features["properties"]['CCG21CD'], 'CCG21CD')
                features['properties'].update({'FID': fid})
                if version == MAP_NORMAL_VER:
                    for var_name in self.dataset_info_oaps[year][quarter].variable_list:
                        features['properties'].update({var_name: self.CCG_FID_get_var(mapped_data, fid, var_name)})
                elif version == MAP_INCREASE_VER:
                    features['properties'].update({'increase': self.CCG_FID_get_var(mapped_data, fid, 'increase')})
        # get a new file name according to the dataset time and other parameters
        file_name = self.choropleth_map_new_geofile_name_get(version, type, year, quarter, var)
        # write combined data into new file
        with open(file_name, 'w') as f:
            json.dump(geo_data, f)

    def choropleth_map_html_file_name_get(self, version, diagnosis, year, quarter, var):
        """
        get new html file name for generated map according to the time and other parameters
        :param version: MAP_NORMAL_VER-normal maps, MAP_INCREASE_VER-maps that represent growth
        :param diagnosis: symbolic constant to identify health diagnosis
        :param year: symbolic constant to identify different years
        :param quarter: symbolic constant to identify different quarters
        :param var: variable name
        :return: file name
        """
        file_name = ''
        name_str = ''
        # add additional string to identify map version
        if version == MAP_INCREASE_VER:
            name_str = '_increase'
        # generate a new html file name according to the dataset time and other parameters
        if diagnosis == DATASET_DIAGNOSIS_IAPT:
            file_name = self.new_file_path + 'iapt_map' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.html'
        elif diagnosis == DATASET_DIAGNOSIS_CYPED:
            file_name = self.new_file_path + 'cyped_map' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.html'
        elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
            file_name = self.new_file_path + 'phsmi_map' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.html'
        elif diagnosis == DATASET_DIAGNOSIS_OAPS:
            file_name = self.new_file_path + 'oaps_map' + f'{year + 2019}_' \
                        + f'quarter{quarter + 1}_' + var + name_str + '.html'
        return file_name

    def variable_list_for_diagnosis_get(self, diagnosis, year, quarter):
        """
        get all the variables for a specific health diagnosis
        :param diagnosis: health diagnosis
        :param year: year
        :param quarter: quarter
        :return: a list of all the variables
        """
        if diagnosis == DATASET_DIAGNOSIS_IAPT:
            return self.dataset_info_iapt[year][quarter].variable_list
        elif diagnosis == DATASET_DIAGNOSIS_CYPED:
            return self.dataset_info_cyped[year][quarter].variable_list
        elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
            return self.dataset_info_phsmi[year][quarter].variable_list
        elif diagnosis == DATASET_DIAGNOSIS_OAPS:
            return self.dataset_info_oaps[year][quarter].variable_list

    def create_choropleth_map(self, type, year, quarter, var):
        """
        create a choropleth map according to the dataset time, health diagnosis, and variable
        :param type: symbolic constant to identify health diagnosis
        :param year: symbolic constant to identify different year
        :param quarter: symbolic constant to identify different quarters
        :param var: variable name
        :return: a map
        """
        dataset = []
        # get codes and names file data
        code_list = self.ccg_code_data[year]
        geo_ccg = 0
        map_title = ''
        data_pd = []

        # for each year, health diagnosis:
        # get codes and names file data with part column
        # and renames dataset column to corresponds to the column name of mapped mental health dataset
        if year == DATASET_TIME_YEAR_2019_20:
            code_list = code_list.drop(['CCG19CD', 'CCG19NM'], axis=1)
            if type == DATASET_DIAGNOSIS_IAPT:
                code_list = code_list.rename(columns={'CCG19CDH': 'CCG'})
            elif type == DATASET_DIAGNOSIS_CYPED or type == DATASET_DIAGNOSIS_PHSMI:
                code_list = code_list.rename(columns={'CCG19CDH': 'CCG Code'})
            elif type == DATASET_DIAGNOSIS_OAPS:
                code_list = code_list.rename(columns={'CCG19CDH': 'Breakdown One Code'})
        elif year == DATASET_TIME_YEAR_2020_21:
            code_list = code_list.drop(['CCG20CD', 'CCG20NM'], axis=1)
            if type == DATASET_DIAGNOSIS_IAPT:
                code_list = code_list.rename(columns={'CCG20CDH': 'CCG'})
            elif type == DATASET_DIAGNOSIS_CYPED or type == DATASET_DIAGNOSIS_PHSMI:
                code_list = code_list.rename(columns={'CCG20CDH': 'CCG Code'})
            elif type == DATASET_DIAGNOSIS_OAPS:
                code_list = code_list.rename(columns={'CCG20CDH': 'Breakdown One Code'})
        elif year == DATASET_TIME_YEAR_2021_22:
            code_list = code_list.drop(['CCG21CD', 'CCG21NM'], axis=1)
            if type == DATASET_DIAGNOSIS_IAPT:
                code_list = code_list.rename(columns={'CCG21CDH': 'CCG'})
            elif type == DATASET_DIAGNOSIS_CYPED or type == DATASET_DIAGNOSIS_PHSMI:
                code_list = code_list.rename(columns={'CCG21CDH': 'CCG Code'})
            elif type == DATASET_DIAGNOSIS_OAPS:
                code_list = code_list.rename(columns={'CCG21CDH': 'Breakdown One Code'})

        # for dataset of each health diagnosis:
        # 1. generate relevant map tile
        # 2. do some data pre-processing
        if type == DATASET_DIAGNOSIS_IAPT:
            map_title = f'Adult with common mental health problems by CCG - Quarter {quarter+1}' \
                        f'{2019+year}/{20+year}'
            dataset = self.dataset_info_iapt[year][quarter].dataset
            dataset = dataset[dataset['GroupType'] == 'CCG']
            dataset = dataset[dataset['VariableType'] == 'Total']
            dataset = dataset.drop_duplicates(['CCG'], keep="first")
            dataset = dataset[dataset['CCG'] != 'NULL']
        elif type == DATASET_DIAGNOSIS_CYPED:
            map_title = f'Children and Young People with an Eating Disorder Waiting Times by CCG' \
                        ' - Quarter {quarter+1} {2019+year}/{20+year}'
            dataset = self.dataset_info_cyped[year][quarter].dataset
        elif type == DATASET_DIAGNOSIS_PHSMI:
            map_title = f'People with severe mental illness to receive physical health checks by CCG' \
                        f' - Quarter {quarter+1} {2019+year}/{20+year}'
            dataset = self.dataset_info_phsmi[year][quarter].dataset
        elif type == DATASET_DIAGNOSIS_OAPS:
            map_title = f'Inappropriate Out of Area Placements in Mental Health Services - Quarter {quarter+1} ' \
                        '{2019+year}/{20+year}'
            dataset = self.dataset_info_oaps[year][quarter].dataset
            dataset = dataset[dataset['Breakdown One'] == 'Ccg']

        # merge dataset and code data
        if type == DATASET_DIAGNOSIS_IAPT:
            data_pd = pd.merge(code_list, dataset, how='left', on=['CCG'])
        elif type == DATASET_DIAGNOSIS_CYPED or type == DATASET_DIAGNOSIS_PHSMI:
            data_pd = pd.merge(code_list, dataset, how='left', on=['CCG Code'])
        elif type == DATASET_DIAGNOSIS_OAPS:
            data_pd = pd.merge(code_list, dataset, how='left', on=['Breakdown One Code'])

        # get new geojson file name
        file_name = self.choropleth_map_new_geofile_name_get(MAP_NORMAL_VER, type, year, quarter, '')
        # check if this geojson file has existed, if not, then generate it
        if not os.path.exists(file_name):
            self.create_new_geojson(MAP_NORMAL_VER, type, year, quarter, '', data_pd)
        # read geospatial data
        geo_ccg = gpd.read_file(file_name)

        # create choropleth map
        m = folium.Map([53, -2], zoom_start=6)
        folium.GeoJson(
            geo_ccg,
            style_function=lambda feature: {
                'color': 'black',
                'weight': 1,
            }
        ).add_to(m)

        # map mental health data onto the map according to column 'FID'
        choropleth_map = folium.Choropleth(
            geo_data=geo_ccg,
            data=data_pd,
            columns=['FID', var],
            key_on='feature.properties.FID',
            fill_color="OrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=map_title,
        ).add_to(m)

        # get variable list to be displayed when hovering
        mouse_over_var_list = []
        if year == DATASET_TIME_YEAR_2019_20:
            mouse_over_var_list = ['CCG19NM']
        elif year == DATASET_TIME_YEAR_2020_21:
            mouse_over_var_list = ['ccg20nm']
        elif year == DATASET_TIME_YEAR_2021_22:
            mouse_over_var_list = ['CCG21NM']
        mouse_over_var_list.append(var)
        var_list = self.variable_list_for_diagnosis_get(type, year, quarter)
        for i in var_list:
            mouse_over_var_list.append(i)
        choropleth_map.geojson.add_child(folium.features.GeoJsonTooltip(mouse_over_var_list))

        # get a new map html file name and save the map with this name
        map_html = self.choropleth_map_html_file_name_get(MAP_NORMAL_VER, type, year, quarter, var)
        m.save(map_html)

        return m

    def create_choropleth_map_increase_ver(self, diagnosis, var, start_year, end_year):
        """
        create a choropleth map with increasing variable year over-year
        according to the dataset time, health diagnosis, and variable
        :param diagnosis: symbolic constant to identify health diagnosis
        :param var: variable name
        :param start_year: start year, symbolic constant to identify different years
        :param end_year: end year, symbolic constant to identify different years
        :return: a map
        """
        geo_ccg = 0
        map_title = ''
        data_pd = []
        code_data = self.ccg_code_data[DATASET_TIME_YEAR_2019_20]
        # dataset which is going to be mapped to the choropleth map
        increase_df = []

        # get the list of common ccg code
        common_code_list = common_ccg_get(COMMON_CCG_CODE, diagnosis)
        # choose code and name file data of 2019 year to be merged as geospatial data
        df = pd.DataFrame(common_code_list, columns=['CCG19CDH'])
        common_code_data = pd.merge(code_data, df, how='left', on=['CCG19CDH'])
        common_code_data = common_code_data.drop(['CCG19CD', 'CCG19NM'], axis=1)
        # get common code and name file data using data of 2019 year
        if diagnosis == DATASET_DIAGNOSIS_IAPT:
            common_code_data = common_code_data.rename(columns={'CCG19CDH': 'CCG'})
        elif diagnosis == DATASET_DIAGNOSIS_CYPED or type == DATASET_DIAGNOSIS_PHSMI:
            common_code_data = common_code_data.rename(columns={'CCG19CDH': 'CCG Code'})
        elif diagnosis == DATASET_DIAGNOSIS_OAPS:
            common_code_data = common_code_data.rename(columns={'CCG19CDH': 'Breakdown One Code'})

        # get dataset 'increase_df' which is going to be mapped onto the choropleth map for IAPT
        # the column 'increase' of the dataset 'increase_df' indicates the color to show focus + context
        if diagnosis == DATASET_DIAGNOSIS_IAPT:
            dataset_group = global_variables.get_value(global_variables.KEY_DATASET_IAPT)
            # create dataset which is going to be mapped onto the choropleth map
            # the value of column 'increase' indicates the color of a CCG region
            increase_df = pd.DataFrame(columns=['CCG', 'increase'])
            # for each CCG
            for ccg in common_code_list:
                value_year_list = []
                # for each year
                for year in range(start_year, end_year + 1):
                    # calculate the total value of a variable for one year
                    value_year = 0
                    for quarter in range(4):
                        dataset = dataset_group[year][quarter].dataset
                        dataset = dataset[dataset['GroupType'] == 'CCG']
                        dataset = dataset[dataset['VariableType'] == 'Total']
                        dataset = dataset[dataset['CCG'] == ccg]
                        for index, row in dataset.iterrows():
                            if row['CCG'] == ccg:
                                value_year += row[var]
                                break
                    # record the value of a variable for each year
                    value_year_list.append(value_year)
                row_list = [ccg]
                increase = 5000
                # user option: focus + context
                # check if the data value is increasing year-over-year, if not, then set 'increase' column to 0
                for i in range(len(value_year_list)):
                    if i+1 < len(value_year_list):
                        if value_year_list[i+1] < value_year_list[i]:
                            increase = 0
                            break
                # write a list [ccg, increase] and create a new row with this list
                row_list.append(increase)
                new_row = tuple(row_list)
                new_row = [new_row]
                # add a new row into dataset 'increase_df'
                ccg_increase = pd.DataFrame(new_row, columns=['CCG', 'increase'])
                increase_df = increase_df.append(ccg_increase, ignore_index=True)
        # get dataset 'increase_df' which is going to be mapped onto the choropleth map for CYPED
        elif diagnosis == DATASET_DIAGNOSIS_CYPED:
            dataset_group = global_variables.get_value(global_variables.KEY_DATASET_CYPED)
            increase_df = pd.DataFrame(columns=['CCG Code', 'increase'])
            for ccg in common_code_list:
                value_year_list = []
                for year in range(start_year, end_year + 1):
                    value_year = 0
                    for quarter in range(4):
                        dataset = dataset_group[year][quarter].dataset
                        dataset = dataset[dataset['CCG Code'] == ccg]
                        for index, row in dataset.iterrows():
                            if row['CCG Code'] == ccg:
                                value_year += row[var]
                                break
                    value_year_list.append(value_year)
                row_list = [ccg]
                increase = 5000
                for i in range(len(value_year_list)):
                    if i + 1 < len(value_year_list) & value_year_list[i + 1] < value_year_list[i]:
                        increase = 0
                        break
                row_list.append(increase)
                new_row = tuple(row_list)
                new_row = [new_row]
                ccg_increase = pd.DataFrame(new_row, columns=['CCG Code', 'increase'])
                increase_df = increase_df.append(ccg_increase, ignore_index=True)
        # get dataset 'increase_df' which is going to be mapped onto the choropleth map for PHSMI
        elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
            dataset_group = global_variables.get_value(global_variables.KEY_DATASET_PHSMI)
            increase_df = pd.DataFrame(columns=['CCG Code', 'increase'])
            for ccg in common_code_list:
                value_year_list = []
                for year in range(start_year, end_year + 1):
                    value_year = 0
                    for quarter in range(4):
                        dataset = dataset_group[year][quarter].dataset
                        dataset = dataset[dataset['CCG Code'] == ccg]
                        for index, row in dataset.iterrows():
                            if row['CCG Code'] == ccg:
                                value_year += row[var]
                                break
                    value_year_list.append(value_year)
                row_list = [ccg]
                increase = 5000
                for i in range(len(value_year_list)):
                    if i + 1 < len(value_year_list) & value_year_list[i + 1] < value_year_list[i]:
                        increase = 0
                        break
                row_list.append(increase)
                new_row = tuple(row_list)
                new_row = [new_row]
                ccg_increase = pd.DataFrame(new_row, columns=['CCG Code', 'increase'])
                increase_df = increase_df.append(ccg_increase, ignore_index=True)
        # get dataset 'increase_df' which is going to be mapped onto the choropleth map for OAPS:
        elif diagnosis == DATASET_DIAGNOSIS_OAPS:
            dataset_group = global_variables.get_value(global_variables.KEY_DATASET_OAPS)
            increase_df = pd.DataFrame(columns=['Breakdown One Code', 'increase'])
            for ccg in common_code_list:
                value_year_list = []
                for year in range(start_year, end_year + 1):
                    value_year = 0
                    for quarter in range(4):
                        dataset = dataset_group[year][quarter].dataset
                        dataset = dataset[dataset['Breakdown One Code'] == ccg]
                        for index, row in dataset.iterrows():
                            if row['Breakdown One Code'] == ccg:
                                value_year += row[var]
                                break
                    value_year_list.append(value_year)
                row_list = [ccg]
                increase = 5000
                for i in range(len(value_year_list)):
                    if i + 1 < len(value_year_list) & value_year_list[i + 1] < value_year_list[i]:
                        increase = 0
                        break
                row_list.append(increase)
                new_row = tuple(row_list)
                new_row = [new_row]
                ccg_increase = pd.DataFrame(new_row, columns=['Breakdown One Code', 'increase'])
                increase_df = increase_df.append(ccg_increase, ignore_index=True)

        if diagnosis == DATASET_DIAGNOSIS_IAPT:
            data_pd = pd.merge(common_code_data, increase_df, how='left', on=['CCG'])
        elif diagnosis == DATASET_DIAGNOSIS_CYPED or diagnosis == DATASET_DIAGNOSIS_PHSMI:
            data_pd = pd.merge(common_code_data, increase_df, how='left', on=['CCG Code'])
        elif diagnosis == DATASET_DIAGNOSIS_OAPS:
            data_pd = pd.merge(common_code_data, increase_df, how='left', on=['Breakdown One Code'])

        shape = data_pd.shape
        for i in range(shape[0]):
            if math.isnan(data_pd.iloc[i, 2]):
                data_pd.iloc[i, 2] = 0

        file_name = self.choropleth_map_new_geofile_name_get(MAP_INCREASE_VER, diagnosis,
                                                             DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER1, var)
        if not os.path.exists(file_name):
            self.create_new_geojson(MAP_INCREASE_VER, diagnosis,
                                    DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER1, var, data_pd)
        geo_ccg = gpd.read_file(file_name)

        # create a choropleth map
        m = folium.Map([53, -2], zoom_start=6)
        folium.GeoJson(
            geo_ccg,
            style_function=lambda feature: {
                'color': 'black',
                'weight': 1,
            }
        ).add_to(m)

        choropleth_map = folium.Choropleth(
            geo_data=geo_ccg,
            data=data_pd,
            columns=['FID', 'increase'],
            key_on='feature.properties.FID',
            fill_color="OrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=map_title,
        ).add_to(m)

        # only display on which CCG the data value is increasing year-over-year
        choropleth_map.geojson.add_child(folium.features.GeoJsonTooltip(['CCG19NM']))

        map_html = self.choropleth_map_html_file_name_get(MAP_INCREASE_VER, diagnosis,
                                                          DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER1, var)
        m.save(map_html)

        return m
