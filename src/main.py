import ui_class
import global_variables
from map_class import *
from ui_class import *
import sys
from data import *


if __name__ == '__main__':
    global_variables._init()

    # create a choropleth map for NHS mental health population data
    myMap = NHSMentalHealthCCGMap()
    myMap.create_choropleth_map(DATASET_DIAGNOSIS_IAPT, DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER1,
                                myMap.dataset_info_iapt[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1].variable_list[DATASET_IAPT_VARIABLE_FIELD_INDEX_START])
    # save as a global variable for further use
    global_variables.set_value(global_variables.KEY_MAP, myMap)

    # create a visualization application
    myApp = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QWidget()
    # create GUI
    ui = MapUi()
    ui.setup_ui(main_window)
    # load map
    ui.load_map(MAP_NORMAL_VER, DATASET_DIAGNOSIS_IAPT, DATASET_TIME_YEAR_2019_20, DATASET_TIME_QUARTER1,
                myMap.dataset_info_iapt[DATASET_TIME_YEAR_2019_20][DATASET_TIME_QUARTER1].variable_list[DATASET_IAPT_VARIABLE_FIELD_INDEX_START])
    # display map
    main_window.show()
    global_variables.set_value(global_variables.KEY_MAIN_WINDOW, main_window)

    try:
        sys.exit(myApp.exec_())
    except SystemExit:
        print('Closing Window...')



