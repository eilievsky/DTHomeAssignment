#-----------------------------------------------------------------------------------------------------
# contains function that should be activated from flask end points
#-----------------------------------------------------------------------------------------------------

import requests
import json
import datetime as dt
import warnings
import processobjects.countries as co
import processobjects.coviddata as cov

# function for /status end point
def get_status():
    try:
        url = "https://api.covid19api.com/summary"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.dumps({"status":"sucess"})
        else:
            return json.dumps({"status":"fail"})
    except:
        return json.dumps({"status": "fail"})

# function for /deathsPeak end point
def get_death_peak(args_dict):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    coun_name = args_dict.get('country','')
    if coun_name == '':
        return json.dumps({"error":"No country defined"})
    coun_obj = co.Countries()
    if coun_obj.get_slug_value(coun_name) == '':
        return json.dumps({"error": f"No such countr {coun_name}"})
    covid_obj = cov.CovidData(country=coun_name, init_date=dt.datetime.now(), days_back=30, coun_obj=coun_obj)
    covid_obj.get_data()
    return json.dumps(covid_obj.get_max_death_record_formatted())

#function for /provinceConfirmedMax
def get_province_confirmed_max():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    coun_obj = co.Countries()
    country_lst = coun_obj.get_country_list()

    max_confirmed_record_lst = []
    for el in country_lst:
        print(f"collecting data for {el}")
        covid_obj = cov.CovidData(country=el, init_date=dt.datetime.now(), days_back=30, coun_obj=coun_obj)
        covid_obj.get_data()
        max_confirmed_record_lst.append(covid_obj.get_max_confirmed_record())

    max_val = 0
    max_val_dict = {}
    for el in max_confirmed_record_lst:
        if el != '':
            if len(el.keys()) > 0:
                if list(el.get('Confirmed_Dif').values())[0] > max_val:
                    max_val = list(el.get('Confirmed_Dif').values())[0]
                    max_val_dict = el

    tmp_country = list(max_val_dict.get('Country').values())[0]
    tmp_province = list(max_val_dict.get('Province').values())[0]
    tmp_value = list(max_val_dict.get('Confirmed_Dif').values())[0]
    tmp_date = list(max_val_dict.get('Date').values())[0]

    cal_result = {'province': tmp_province, 'country': tmp_country, 'date': tmp_date, 'value': tmp_value}
    return json.dumps(cal_result)










