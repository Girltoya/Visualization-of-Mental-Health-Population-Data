import pandas as pd
import csv
import xlrd


# geospatial file path
GEO_JASON_FILE_DIR = 'CCG_GEO/'
# geospatial file name (gejson file)
GEO_JASON_FILE_NAME_2019 = 'Clinical_Commissioning_Groups_(April_2019)_Boundaries_EN_BGC.geojson'
GEO_JASON_FILE_NAME_2020 = 'Clinical_Commissioning_Groups_(April_2020)_EN_BFC_V2.geojson'
GEO_JASON_FILE_NAME_2021 = 'Clinical_Commissioning_Groups_(April_2021)_EN_BFC.geojson'
# code and name file name
CCG_NAMES_AND_CODES_FILE_NAME_2019 = 'Clinical_Commissioning_Groups_(April_2019)_Names_and_Codes_in_England.csv'
CCG_NAMES_AND_CODES_FILE_NAME_2020 = 'Clinical_Commissioning_Groups_(April_2020)_Names_and_Codes_in_England.csv'
CCG_NAMES_AND_CODES_FILE_NAME_2021 = 'Clinical_Commissioning_Groups_(April_2021)_Names_and_Codes_in_England.csv'
# Mental health population data file
# file path for health diagnosis: IAPT
DATASET_IAPT_FILE_DIR = 'IAPT/'
# Mental health population data file for IAPT
DATASET_IAPT_FILE_NAME_2019_20_QUARTER1 = 'iapt-quarter-q1-2019-20-final-data.csv'
DATASET_IAPT_FILE_NAME_2019_20_QUARTER2 = 'iapt-quarter-q2-2019-20-final-data.csv'
DATASET_IAPT_FILE_NAME_2019_20_QUARTER3 = 'iapt-quarter-q3-2019-20-final-data.csv'
DATASET_IAPT_FILE_NAME_2019_20_QUARTER4 = 'iapt-quarter-q4-2019-20-final-data.csv'
DATASET_IAPT_FILE_NAME_2020_21_QUARTER1 = 'iapt-quarter-q1-2020-21-v2.csv'
DATASET_IAPT_FILE_NAME_2020_21_QUARTER2 = 'iapt-quarter-q1-2020-21-v2.csv'
DATASET_IAPT_FILE_NAME_2020_21_QUARTER3 = 'iapt-quarter-q3-2020-21-final-data.csv'
DATASET_IAPT_FILE_NAME_2020_21_QUARTER4 = 'iapt-quarter-q4-2020-21-final-data.csv'
DATASET_IAPT_FILE_NAME_2021_22_QUARTER1 = 'iapt-quarter-q1-2021-22-final-data.csv'
DATASET_IAPT_FILE_NAME_2021_22_QUARTER2 = 'iapt-quarter-q2-2021-22-final-data.csv'
DATASET_IAPT_FILE_NAME_2021_22_QUARTER3 = 'iapt-quarter-q3-2021-22-final-data.csv'
DATASET_IAPT_FILE_NAME_2021_22_QUARTER4 = 'iapt-quarter-q4-2021-22-final-data.csv'
# file path for health diagnosis: CYPED
DATASET_CYPED_FILE_DIR = 'CYPED/'
# Mental health population data file for CYPED
DATASET_CYPED_FILE_NAME_2019_20_QUARTER1 = 'CYPED-Publication-Q1-2019-20-Provider-CCG-new-codes-3.xls'
DATASET_CYPED_FILE_NAME_2019_20_QUARTER2 = 'CYPED-Publication-Q2-2019-20-Provider-CCG-new-codes.xls'
DATASET_CYPED_FILE_NAME_2019_20_QUARTER3 = 'CYPED-Publication-Q3-2019-20-Provider-CCG-new-codes-CORRECT-13022020.xls'
DATASET_CYPED_FILE_NAME_2019_20_QUARTER4 = 'CYPED-Publication-Q4-2019-20-Provider-CCG-new-codes-NEW.xls'
DATASET_CYPED_FILE_NAME_2020_21_QUARTER1 = 'CYPED-Publication-Q1-2020-21-Provider-CCG-new-codes.xls'
DATASET_CYPED_FILE_NAME_2020_21_QUARTER2 = 'CYPED-Publication-Q2-2020-21-Provider-CCG-new-codes-1.xlsx'
DATASET_CYPED_FILE_NAME_2020_21_QUARTER3 = 'CYPED-Publication-Q3-2020-21-Provider-CCG-new-codes.xlsx'
DATASET_CYPED_FILE_NAME_2020_21_QUARTER4 = 'CYPED-Publication-Q4-2020-21-Provider-CCG.xlsx'
DATASET_CYPED_FILE_NAME_2021_22_QUARTER1 = 'CYPED-Publication-Q1-2021-22-Provider-CCG-new-codes.xlsx'
DATASET_CYPED_FILE_NAME_2021_22_QUARTER2 = 'CYPED-Publication-Q2-2021-22-Provider-CCG-new-codes-v2-1.xlsx'
DATASET_CYPED_FILE_NAME_2021_22_QUARTER3 = 'CYPED-Publication-Q3-2021-22-Provider-CCG-new-codes-v2.xlsx'
DATASET_CYPED_FILE_NAME_2021_22_QUARTER4 = 'CYPED-Publication-Q4-2021-22-Provider-CCG-new-codes.xlsx'
# file path for health diagnosis: PHSMI
DATASET_PHSMI_FILE_DIR = 'PHSMI/'
# Mental health population data file for PHSMI
DATASET_PHSMI_FILE_NAME_2019_20_QUARTER1 = 'Physical-Health-Checks-SMI-Q1-2019-20-v1.0.xlsx'
DATASET_PHSMI_FILE_NAME_2019_20_QUARTER2 = 'Physical-Health-Checks-SMI-Q2-2019-20-v1.0.xlsx'
DATASET_PHSMI_FILE_NAME_2019_20_QUARTER3 = 'Physical-Health-Checks-SMI-Q3-2019-20-v1.0.xlsx'
DATASET_PHSMI_FILE_NAME_2019_20_QUARTER4 = 'Physical-Health-Checks-SMI-Q4-2019-20-v1.0.xlsx'
DATASET_PHSMI_FILE_NAME_2020_21_QUARTER1 = 'Physical-Health-Checks-SMI-Q1-2020-21-v1.0.xlsx'
DATASET_PHSMI_FILE_NAME_2020_21_QUARTER2 = 'Physical-Health-Checks-SMI-Q2-2020-21-v1.1-1.xlsx'
DATASET_PHSMI_FILE_NAME_2020_21_QUARTER3 = 'Physical-Health-Checks-SMI-Q3-2020-21.xlsx'
DATASET_PHSMI_FILE_NAME_2020_21_QUARTER4 = 'Physical-Health-Checks-SMI-Q4-2020-21.xlsx'
DATASET_PHSMI_FILE_NAME_2021_22_QUARTER1 = 'Physical-Health-Checks-SMI-Q1-2021-22.xlsx'
DATASET_PHSMI_FILE_NAME_2021_22_QUARTER2 = 'Physical-Health-Checks-SMI-Q2-2021-22.xlsx'
DATASET_PHSMI_FILE_NAME_2021_22_QUARTER3 = 'Physical-Health-Checks-SMI-Q3-2021-22.xlsx'
DATASET_PHSMI_FILE_NAME_2021_22_QUARTER4 = 'Physical-Health-Checks-SMI-Q4-2021-22.xlsx'
# file path for health diagnosis: OAPS
DATASET_OAPS_FILE_DIR = 'OAPS/'
# Mental health population data file for OAPS
DATASET_OAPS_FILE_NAME_2019_20_QUARTER1 = 'oaps-additional-data-mar-2019.xlsx'
DATASET_OAPS_FILE_NAME_2019_20_QUARTER2 = 'oaps-additional-data-Jun-2019.xlsx'
DATASET_OAPS_FILE_NAME_2019_20_QUARTER3 = 'oaps-additional-data-sep-2019.xlsx'
DATASET_OAPS_FILE_NAME_2019_20_QUARTER4 = 'oaps-additional-data-dec-2019.xlsx'
DATASET_OAPS_FILE_NAME_2020_21_QUARTER1 = 'oaps-additional-data-mar-2020.xlsx'
DATASET_OAPS_FILE_NAME_2020_21_QUARTER2 = 'oaps-additional-data-jun-2020.xlsx'
DATASET_OAPS_FILE_NAME_2020_21_QUARTER3 = 'oaps-additional-data-sep-2020.xlsx'
DATASET_OAPS_FILE_NAME_2020_21_QUARTER4 = 'oaps-additional-data-dec-2020.xlsx'
DATASET_OAPS_FILE_NAME_2021_22_QUARTER1 = 'oaps-additional-data-mar-2021.xlsx'
DATASET_OAPS_FILE_NAME_2021_22_QUARTER2 = 'oaps-additional-data-jun-2021.xlsx'
DATASET_OAPS_FILE_NAME_2021_22_QUARTER3 = 'oaps-additional-data-sep-2021.xlsx'
DATASET_OAPS_FILE_NAME_2021_22_QUARTER4 = 'oaps-additional-data-dec-2021.xlsx'

# index of the first variable in column name list
DATASET_IAPT_VARIABLE_FIELD_INDEX_START = 11
DATASET_CYPED_VARIABLE_FIELD_INDEX_START = 4
DATASET_PHSMI_VARIABLE_FIELD_INDEX_START = 4
DATASET_OAPS_VARIABLE_FIELD_INDEX_START = 5

# string name for each health diagnosis
DATASET_DIAGNOSIS_IAPT_STR = 'Adult Mental Health (common mental health problems)'
DATASET_DIAGNOSIS_CYPED_STR = 'Children and Young People Mental Health-Eating Disorder Waiting Times'
DATASET_DIAGNOSIS_PHSMI_STR = 'Physical health checks for people with severe mental illness'
DATASET_DIAGNOSIS_OAPS_STR = 'Out of Area Placements in Mental Health Services'
# symbolic constants to identify health diagnoses
DATASET_DIAGNOSIS_IAPT = 0
DATASET_DIAGNOSIS_CYPED = 1
DATASET_DIAGNOSIS_PHSMI = 2
DATASET_DIAGNOSIS_OAPS = 3

# symbolic constants to identify time (year, quarter)
DATASET_TIME_YEAR_2019_20 = 0
DATASET_TIME_YEAR_2020_21 = 1
DATASET_TIME_YEAR_2021_22 = 2
DATASET_TIME_QUARTER1 = 0
DATASET_TIME_QUARTER2 = 1
DATASET_TIME_QUARTER3 = 2
DATASET_TIME_QUARTER4 = 3

# dictionary of corresponding relationships between variables and its code
var_dic = {'M001': 'ReferralsReceived', 'M031': 'FirstTreatment', 'M075': 'EndedTreatedOnce',
           'M076': 'FinishedCourseTreatment', 'M179': 'NotCaseness', 'M191': 'Recovery',
           'M185': 'Improvement', 'M189': 'Deterioration', 'M187': 'NoReliableChange',
           'M193': 'ReliableRecovery', 'M052': 'FirstTreatment6WeeksFinishedCourse',
           'M054': 'FirstTreatment18WeeksFinishedCourse', 'M192': 'RecoveryRate', 'M186': 'ImprovementRate',
           'M195': 'ReliableRecoveryRate', 'M053': 'FirstTreatment6WeeksFinishedCourseRate', 'M055': 'FirstTreatment18WeeksFinishedCourseRate',
           'M204': 'CountAppropriatePairedADSM', 'M203': 'CountADSMFinishedTreatment', 'M205': 'PercentageAppropriatePairedADSM'}

# dictionary of corresponding relationships between variables and its symbolic constant
index_dic = {'ReferralsReceived': 0, 'FirstTreatment': 1, 'EndedTreatedOnce': 2,
             'FinishedCourseTreatment': 3, 'NotCaseness': 4, 'Recovery': 5,
             'Improvement': 6, 'Deterioration': 7, 'NoReliableChange': 8,
             'ReliableRecovery': 9, 'ProbDescMeanSession': 10, 'FirstTreatment6WeeksFinishedCourse': 11,
             'FirstTreatment18WeeksFinishedCourse': 12, 'RecoveryRate': 13, 'ImprovementRate': 14,
             'ReliableRecoveryRate': 15, 'FirstTreatment6WeeksFinishedCourseRate': 16,
             'FirstTreatment18WeeksFinishedCourseRate': 17, 'CountAppropriatePairedADSM': 18,
             'CountADSMFinishedTreatment': 19, 'PercentageAppropriatePairedADSM': 20}


class DatasetInfo:
    """
    Class for the information of dataset, recording details about mental health population data
    """
    def __init__(self, dataset_path, diagnosis, year, quarter):
        # store data in dataframe format read from data files
        self.dataset = []
        # store variables of the dataset for a specific health diagnosis
        self.variable_list = []
        # get the list of variables for each health diagnosis
        if diagnosis == DATASET_DIAGNOSIS_IAPT:
            self.dataset = pd.read_csv(dataset_path)
            self.variable_list = self.dataset.columns.values[DATASET_IAPT_VARIABLE_FIELD_INDEX_START:]
        elif diagnosis == DATASET_DIAGNOSIS_CYPED:
            excel = xlrd.open_workbook(dataset_path)
            self.dataset = excel.sheet_by_index(1)
            # the dataset is unusual, the list of variables need to be written manually
            heads = ['Region Code', 'STP Code', 'CCG Code', 'CCG Name', '>0-1 week (urgent)', '>1-4 weeks (urgent)',
                                  '>4-12 weeks (urgent)', '12 plus (urgent)',
                                  'Total number of completed pathways (urgent)', '% within 1 week (urgent)',
                                  '>0-1 week (routine)', '>1-4 weeks (routine)',
                                  '>4-12 weeks (routine)', '12 plus (routine)',
                                  'Total number of completed pathways (routine)', '% within 4 weeks (routine)']
            self.variable_list = heads[DATASET_CYPED_VARIABLE_FIELD_INDEX_START:]
            # the dataset is unusual, a new dataframe need to be created to combine several tables in the same format
            new_df = pd.DataFrame(columns=heads)
            # dataset of different year for the same health diagnosis has different numbers of records
            start_row = 15
            end_row = 0
            if year == DATASET_TIME_YEAR_2019_20:
                end_row = 207
            elif year == DATASET_TIME_YEAR_2020_21:
                end_row = 151
            elif year == DATASET_TIME_YEAR_2021_22:
                end_row = 122
            for i in range(start_row, end_row):
                list = []
                for j in range(1, 18):
                    if j != 11:
                        list.append(self.dataset.cell(i, j).value)
                new_row = tuple(list)
                new_row = [new_row]
                new_row = pd.DataFrame(new_row, columns=heads)
                new_df = new_df.append(new_row, ignore_index=True)
            self.dataset = new_df
        elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
            excel = xlrd.open_workbook(dataset_path)
            self.dataset = excel.sheet_by_index(2)
            heads = ['Region Code', 'Region Name', 'CCG Code', 'CCG Name',
                     'Numerator (total number to get full check)', 'Denominator',
                     'Alcohol', 'Blood glucose', 'Blood lipid', 'Blood Pressure', 'BMI Weight', 'Smoking']
            self.variable_list = heads[DATASET_PHSMI_VARIABLE_FIELD_INDEX_START:]
            # the dataset is unusual, a new dataframe need to be created to combine several tables in the same format
            new_df = pd.DataFrame(columns=heads)
            # dataset of different year for the same health diagnosis has different numbers of records
            start_row = 15
            end_row = 0
            if year == DATASET_TIME_YEAR_2019_20:
                end_row = 206
            elif year == DATASET_TIME_YEAR_2020_21:
                end_row = 150
            elif year == DATASET_TIME_YEAR_2021_22:
                end_row = 121
            for i in range(start_row, end_row):
                list = []
                for j in range(1, 16):
                    if year == 2 and quarter >= 1:
                        if j != 6 and j != 8 and j != 9:
                            list.append(self.dataset.cell(i, j).value)
                    else:
                        if j != 5 and j != 8 and j != 9:
                            list.append(self.dataset.cell(i, j).value)
                new_row = tuple(list)
                new_row = [new_row]
                new_row = pd.DataFrame(new_row, columns=heads)
                new_df = new_df.append(new_row, ignore_index=True)
            self.dataset = new_df
        elif diagnosis == DATASET_DIAGNOSIS_OAPS:
            excel = xlrd.open_workbook(dataset_path)
            self.dataset = excel.sheet_by_index(6)
            # the dataset is unusual, the list of variables need to be written manually
            heads = ['Period Type', 'Period Covered', 'Breakdown One', 'Breakdown One Code',
                     'Breakdown One Description', 'Number of inappropriate OAP days in the period',
                     'Inappropriate OAPs active at period end', 'Number of inappropriate OAPs started in period',
                     'Inappropriate OAPs ended during period',
                     'Number of inappropriate OAPs that ended in the period with a length of 1-7 nights(5)',
                     'Number of inappropriate OAPs that ended in the period with a length of 8-14 nights(5)',
                     'Number of inappropriate OAPs that ended in the period with a length of 15-30 nights(5)',
                     'Number of inappropriate OAPs that ended in the period with a length of 31-90 nights(5)',
                     'Number of inappropriate OAPs that ended in the period with a length of 91 or more nights(5)',
                     'Number of inappropriate OAPs active during the period with a distance of less than 25 km',
                     'Number of inappropriate OAPs active during the period with distance of 25km or greater and less than 50km',
                     'Number of inappropriate OAPs active during the period with a distance of 50km or greater and less than 100km',
                     'Number of inappropriate OAPs active during the period with a distance of 100km or greater and less than 200km',
                     'Number of inappropriate OAPs active during the period with a distance of 200km or greater and less than 300km',
                     'Number of inappropriate OAPs active during the period with a distance of 300km or greater',
                     'Percentage of inappropriate OAP days in the period: external (6)',
                     'Percentage of inappropriate OAP days in the period: private providers',
                     'Percentage of inappropriate OAP days in the period: Acute Adult Mental Health Care',
                     'Percentage of inappropriate OAP days in the period: Acute Older Adult Mental Health Care (organic and functional)',
                     'Percentage of inappropriate OAP days in the period: Psychiatric Intensive Care Unit (acute mental health care)',
                     'Total cost for Inappropriate OAPs in the period(8)(9)', 'Average cost per bed day (7)(8)']
            self.variable_list = heads[DATASET_OAPS_VARIABLE_FIELD_INDEX_START:]
            # the dataset is unusual, a new dataframe need to be created to combine several tables in the same format
            new_df = pd.DataFrame(columns=heads)
            # dataset of different year for the same health diagnosis has different numbers of records
            start_row = 9
            end_row = 0
            if year == DATASET_TIME_YEAR_2019_20:
                end_row = 435
            elif year == DATASET_TIME_YEAR_2020_21:
                end_row = 425
            elif year == DATASET_TIME_YEAR_2021_22:
                if quarter == 3:
                    end_row = 354
                else:
                    end_row = 457
            for i in range(start_row, end_row):
                list = []
                for j in range(0, 27):
                    list.append(self.dataset.cell(i, j).value)
                new_row = tuple(list)
                new_row = [new_row]
                new_row = pd.DataFrame(new_row, columns=heads)
                new_df = new_df.append(new_row, ignore_index=True)
            self.dataset = new_df

        self.type = diagnosis
        self.year = year
        self.quarter = quarter
        self.distribution_type = ['Age', 'Gender', 'Ethnicity']

