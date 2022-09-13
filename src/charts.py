
import pygal
from pygal.style import Style
import plotly.graph_objects as go
from data import *
import global_variables
import plotly.express as px
from map_class import *
TREEMAP_MAX_COLOR_RANGE = 1000


def dataset_cyped_name_19convert21(dataset19, dataset21, ccg_name19):
    """
    because for CYPED, the ccg name of 2021 year is different from that of 2019 year
    we need to get corresponding code name of 2021 year with that of 2019 year
    :param dataset19:
    :param dataset21:
    :param ccg_name19:
    :return:
    """
    code = ''
    for index, row in dataset19.iterrows():
        if row['CCG Name'] == ccg_name19:
            code = row['CCG Code']
            break
    for index, row in dataset21.iterrows():
        if row['CCG Code'] == code:
            return row['CCG Name']
    return ''


def create_dataframe_for_diagnosis(ccg, diagnosis, start_year, end_year):
    """
    create a new dataframe suitable for the visualization of treemap for a CCG with original dataframe
    :param ccg: ccg name
    :param diagnosis: symbolic constant to identify health diagnosis
    :param start_year: start year, symbolic constant to identify years
    :param end_year: end year, symbolic constant to identify years
    :return: new dataframe suitable for the visualization of treemap
    """
    if start_year > end_year:
        return None
    df = pd.DataFrame(columns=['variable', 'year', 'value'])

    # create new dataframe for IAPT
    if diagnosis == DATASET_DIAGNOSIS_IAPT:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_IAPT)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_IAPT_VARIABLE_FIELD_INDEX_START:]

        # for each variable
        for var in vars_list:
            if var == 'ProbDescMeanSession':
                continue
            # for each year
            for year in range(start_year, end_year+1):
                row_list = []
                value_year = 0
                # calculate the total value for one year
                for quarter in range(4):
                    dataset = dataset_group[year][quarter].dataset
                    dataset = dataset[dataset['GroupType'] == 'CCG']
                    dataset = dataset[dataset['VariableType'] == 'Total']
                    dataset = dataset[dataset['CCGName'] == ccg]
                    for index, row in dataset.iterrows():
                        if row['CCGName'] == ccg:
                            value_year += row[var]
                            break
                # in treemap, value zero can not be visualized
                if value_year == 0:
                    value_year = 0.1
                # for each row add a variable name
                row_list.append(var)
                # for each row add a label for the total value of one year
                row_list.append(f'{var}: {2019+year} year')
                # for each row add a total value for one year
                row_list.append(value_year)
                # generate a new row and write it into the new dataframe
                new_row = tuple(row_list)
                new_row = [new_row]
                df_year = pd.DataFrame(new_row, columns=['variable', 'year', 'value'])
                df = df.append(df_year, ignore_index=True)
    # create new dataframe for CYPED with a slight difference
    elif diagnosis == DATASET_DIAGNOSIS_CYPED:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_CYPED)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_CYPED_VARIABLE_FIELD_INDEX_START:]

        for var in vars_list:
            for year in range(start_year, end_year+1):
                row_list = []
                value_year = 0
                # the ccg name of 2021 year is different from that of 2019 year
                # so we need to get the right ccg name for 2021 year according to that of 2019 year
                if year == DATASET_TIME_YEAR_2021_22:
                    new_ccg = dataset_cyped_name_19convert21(dataset_group[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1].dataset,
                                                             dataset_group[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER1].dataset,
                                                             ccg)
                else:
                    new_ccg = ccg
                for quarter in range(4):
                    dataset = dataset_group[year][quarter].dataset
                    dataset = dataset[dataset['CCG Name'] == new_ccg]
                    for index, row in dataset.iterrows():
                        if row['CCG Name'] == new_ccg:
                            value_year += row[var]
                            break
                if value_year == 0:
                    value_year = 0.1
                row_list.append(var)
                row_list.append(f'{var}: {2019 + year} year')
                row_list.append(value_year)
                new_row = tuple(row_list)
                new_row = [new_row]
                df_year = pd.DataFrame(new_row, columns=['variable', 'year', 'value'])
                df = df.append(df_year, ignore_index=True)
    # create new dataframe for PHSMI with a slight difference
    elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_PHSMI)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_PHSMI_VARIABLE_FIELD_INDEX_START:]

        for var in vars_list:
            for year in range(start_year, end_year+1):
                row_list = []
                value_year = 0
                for quarter in range(4):
                    dataset = dataset_group[year][quarter].dataset
                    dataset = dataset[dataset['CCG Name'] == ccg]
                    for index, row in dataset.iterrows():
                        if row['CCG Name'] == ccg:
                            value_year += row[var]
                            break
                if value_year == 0:
                    value_year = 0.1
                row_list.append(var)
                row_list.append(f'{var}: {2019 + year} year')
                row_list.append(value_year)
                new_row = tuple(row_list)
                new_row = [new_row]
                df_year = pd.DataFrame(new_row, columns=['variable', 'year', 'value'])
                df = df.append(df_year, ignore_index=True)
    # create new dataframe for OAPS with a slight difference
    elif diagnosis == DATASET_DIAGNOSIS_OAPS:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_OAPS)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_OAPS_VARIABLE_FIELD_INDEX_START:20]

        for var in vars_list:
            for year in range(start_year, end_year+1):
                row_list = []
                value_year = 0
                for quarter in range(4):
                    dataset = dataset_group[year][quarter].dataset
                    dataset = dataset[dataset['Breakdown One Description'] == ccg]
                    for index, row in dataset.iterrows():
                        if row['Breakdown One Description'] == ccg:
                            value_year += row[var]
                            break
                if value_year == 0:
                    value_year = 0.1
                row_list.append(var)
                row_list.append(f'{var}: {2019 + year} year')
                row_list.append(value_year)
                new_row = tuple(row_list)
                new_row = [new_row]
                df_year = pd.DataFrame(new_row, columns=['variable', 'year', 'value'])
                df = df.append(df_year, ignore_index=True)
    return df


def create_dataframe_for_diagnosis_all_ccg(diagnosis, start_year, end_year):
    """
    create a new dataframe suitable for the visualization of treemap containing all the CCGs
    :param diagnosis: symbolic constant to identify health diagnosis
    :param start_year: start year, symbolic constant to identify years
    :param end_year: end year, symbolic constant to identify years
    :return: a new dataframe suitable for the visualization of treemap containing all the CCGs
    """
    if start_year > end_year:
        return None
    df = pd.DataFrame(columns=['ccg', 'variable', 'year', 'value'])
    ccg_list = common_ccg_get(COMMON_CCG_NAME, diagnosis)
    # create new dataframe for IAPT
    if diagnosis == DATASET_DIAGNOSIS_IAPT:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_IAPT)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_IAPT_VARIABLE_FIELD_INDEX_START:]
        # for each ccg
        for ccg in ccg_list:
            # for each variable
            for var in vars_list:
                if var == 'ProbDescMeanSession':
                    continue
                # for each year
                for year in range(start_year, end_year+1):
                    row_list = []
                    value_year = 0
                    # calculate a total value for one year
                    for quarter in range(4):
                        dataset = dataset_group[year][quarter].dataset
                        dataset = dataset[dataset['GroupType'] == 'CCG']
                        dataset = dataset[dataset['VariableType'] == 'Total']
                        dataset = dataset[dataset['CCGName'] == ccg]
                        for index, row in dataset.iterrows():
                            if row['CCGName'] == ccg:
                                value_year += row[var]
                                break
                    if value_year == 0:
                        value_year = 0.1
                    # for each row add a ccg name
                    row_list.append(ccg)
                    # for each row add a variable name
                    row_list.append(var)
                    # for each row add a label for the total value of one year
                    row_list.append(f'{var}: {2019+year} year')
                    # for each row add the total value of one year
                    row_list.append(value_year)
                    # generate a new row and write it into the new dataframe
                    new_row = tuple(row_list)
                    new_row = [new_row]
                    df_year = pd.DataFrame(new_row, columns=['ccg', 'variable', 'year', 'value'])
                    df = df.append(df_year, ignore_index=True)
    '''elif diagnosis == DATASET_DIAGNOSIS_CYPED:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_CYPED)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_CYPED_VARIABLE_FIELD_INDEX_START:]

        for var in vars_list:
            for year in range(start_year, end_year+1):
                row_list = []
                value_year = 0
                if year == DATASET_TIME_YEAR_2021_22:
                    new_ccg = dataset_cyped_name_19convert21(dataset_group[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1].dataset,
                                                             dataset_group[DATASET_TIME_YEAR_2021_22][DATASET_TIME_QUARTER1].dataset,
                                                             ccg)
                else:
                    new_ccg = ccg
                for quarter in range(4):
                    dataset = dataset_group[year][quarter].dataset
                    dataset = dataset[dataset['CCG Name'] == new_ccg]
                    for index, row in dataset.iterrows():
                        if row['CCG Name'] == new_ccg:
                            value_year += row[var]
                            break
                if value_year == 0:
                    value_year = 0.1
                row_list.append(var)
                row_list.append(f'{var}: {2019 + year} year')
                row_list.append(value_year)
                new_row = tuple(row_list)
                new_row = [new_row]
                df_year = pd.DataFrame(new_row, columns=['variable', 'year', 'value'])
                df = df.append(df_year, ignore_index=True)
    elif diagnosis == DATASET_DIAGNOSIS_PHSMI:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_PHSMI)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_PHSMI_VARIABLE_FIELD_INDEX_START:]

        for var in vars_list:
            for year in range(start_year, end_year+1):
                row_list = []
                value_year = 0
                for quarter in range(4):
                    dataset = dataset_group[year][quarter].dataset
                    dataset = dataset[dataset['CCG Name'] == ccg]
                    for index, row in dataset.iterrows():
                        if row['CCG Name'] == ccg:
                            value_year += row[var]
                            break
                if value_year == 0:
                    value_year = 0.1
                row_list.append(var)
                row_list.append(f'{var}: {2019 + year} year')
                row_list.append(value_year)
                new_row = tuple(row_list)
                new_row = [new_row]
                df_year = pd.DataFrame(new_row, columns=['variable', 'year', 'value'])
                df = df.append(df_year, ignore_index=True)
    elif diagnosis == DATASET_DIAGNOSIS_OAPS:
        dataset_group = global_variables.get_value(global_variables.KEY_DATASET_OAPS)
        vars_list = dataset_group[0][0].dataset.columns[DATASET_OAPS_VARIABLE_FIELD_INDEX_START:20]

        for var in vars_list:
            for year in range(start_year, end_year+1):
                row_list = []
                value_year = 0
                for quarter in range(4):
                    dataset = dataset_group[year][quarter].dataset
                    dataset = dataset[dataset['Breakdown One Description'] == ccg]
                    for index, row in dataset.iterrows():
                        if row['Breakdown One Description'] == ccg:
                            value_year += row[var]
                            break
                if value_year == 0:
                    value_year = 0.1
                row_list.append(var)
                row_list.append(f'{var}: {2019 + year} year')
                row_list.append(value_year)
                new_row = tuple(row_list)
                new_row = [new_row]
                df_year = pd.DataFrame(new_row, columns=['variable', 'year', 'value'])
                df = df.append(df_year, ignore_index=True)'''
    return df


def dataframe_for_diagnosis_add_color_column(df):
    """
    add a color column into a dataframe for a specific health diagnosis
    :param df: a dataframe to be added into a color column
    :return: a new dataframe
    """
    new_df = df.copy()
    # use the value of 'value' column as the value of 'color' column
    new_df['color'] = df['value']
    val_len = len(new_df['value'])
    for i in range(val_len):
        # every three values are the list of values for three years
        if (i + 1) % 3 == 0:
            # if the data is not increasing year-over-year, then set the value of 'color' column to 5
            # set value 5 because the value zero can not be visualized in Plotly
            if new_df['value'][i] < new_df['value'][i - 1] or new_df['value'][i - 1] < \
                    new_df['value'][i - 2]:
                new_df['color'][i] = 5
                new_df['color'][i - 1] = 5
                new_df['color'][i - 2] = 5
    return new_df


def create_tree_map_by_year(diagnosis, start_year, end_year):
    """
    create time-oriented treemap visualizing data with a start year and a end year
    :param diagnosis: symbolic constant to identify health diagnosis
    :param start_year: start year, symbolic constant to identify years
    :param end_year: end year, symbolic constant to identify years
    :return: figure
    """
    # create a new dataframe suitable for the visualization of treemap containing all the CCGs information
    df = create_dataframe_for_diagnosis_all_ccg(diagnosis, start_year, end_year)
    # add the root category
    df["England"] = "England"
    # init hierarchical path
    fig = px.treemap(df, path=['England', 'ccg', 'variable', 'year'], values='value')
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig


def create_tree_map_by_year_increasement(diagnosis, start_year, end_year):
    """
    create time-oriented treemap visualizing data with a start year and a end year (increase only)
    :param diagnosis: symbolic constant to identify health diagnosis
    :param start_year: start year, symbolic constant to identify years
    :param end_year: end year, symbolic constant to identify years
    :return: figure
    """
    global TREEMAP_MAX_COLOR_RANGE
    # create a new dataframe suitable for the visualization of treemap containing all the CCGs information
    df = create_dataframe_for_diagnosis_all_ccg(diagnosis, start_year, end_year)
    df = dataframe_for_diagnosis_add_color_column(df)
    # add the root category
    df["England"] = "England"
    # init hierarchical path
    fig = px.treemap(df, path=['England', 'ccg', 'variable', 'year'], values='value', color='color',
                     color_continuous_scale='Blues', range_color=[0, TREEMAP_MAX_COLOR_RANGE])
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig
