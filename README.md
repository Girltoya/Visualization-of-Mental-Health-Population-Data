# Visualization-of-Mental-Health-Population-Data
This is the visualization project for NHS Mental health population data, the main purpose of which is to develop a noval visualization application 
to visualize NHS Mental health population data and to allow users to do further exploration.
  1. Data Source: NHS Mental health Dashboard
     https://www.england.nhs.uk/publication/nhs-mental-health-dashboard/
  2. Geospatial data source: Boundaries file + Names and Codes file
     https://geoportal.statistics.gov.uk/search?q=Clinical%20Commissioning%20Groups%20generalised%20Clipped%20Boundaries%20in%20England
  3. Development language: Python

Project Work Directory:
1. data: store NHS Mental health population data
2. newfile: store new data files generated during the visualization, including map html files and new geojson files
3. src: store source code

Src Directory:
1. global_variables.py: set and get global varaibles
2. data.py: store any classes and definition about datafiles (source data)
3. main.py: run the visualization application
4. map_class.py: store any classes and API about creating a map
5. ui_class.py: store any classes and API about GUI
6. charts.py: store API about charts

User Manual:
1. development platform: PyCharm
2. pull the whole project to your computer
3. use PyCharm to open the project
4. install neccessary python libraries for running successfully
5. click 'run' to run the application

Notes: due to a large number of data files to read and do data pre-processing at first, 
       it will cost a lot of time to open the application.
