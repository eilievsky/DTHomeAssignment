# Digital Turbine Home Assignment

## Design

### General Explanation
Implementation Covid 19 API data analysis contains deveral parts
- Connection to API (https://api.covid19api.com/) for data collection
- Initializing endpoints
- Data processing engine for analitical results


### Technical Design
Implementation was doone using Flask framework and pandas for data manipulation
Following endpoints defined
- /status
- /deathsPeak (with parameters country=<country>)
- /provinceConfirmedMax



### Code structure

There are several directories:
- appflow - contain files with definition of endpoint flow
  - flowfunctions.py - contans function for endpoint flow.
- constant - contains file with constants 
  - constants.py - contains list of constants that are used in the system (can be replaced with cinfig file structure)
- processobjects - contains files for data processing
  - countries.py - contains definition of country objects that should be used for data processing
  - coviddata.py - contains class for definiotn of covid data objeect collection
  - darefunctions.py - contains functions for date procesing
- test - contains files for testing
  - test.py - manual testings (should not be used)
- main.py - application starting point  (Flask framework definition)

More comments dan be found inside code

### Problems
- API is working very slow and have lot of timeouts
- There is a limitation for API that not allowing retruve data for more thena week for specific countries
- Not for all data defined province. Incide application was implemented logic that set provice as a country in case province is empty

## Improvments
- Errors should be recorded into proper log for analysis (in case of timeout or API errors)
- For province data analysis parallel processing should be used for better performance
- Some values should be defined inconfig files and as a constant for better maintanance
- Since data that is used mostly historical it can be extracted as batch process , stored in more fast persistant and aggrigated for future usage


