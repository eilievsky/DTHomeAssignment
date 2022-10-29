#---------------------------------------------------------------------------------------------
# this file contains definiotn of class that supose to contains data retrived from API reqiest
# this class contains function that allow to perform data analitics calculation
#---------------------------------------------------------------------------------------------


import requests
import pandas as pd
import processobjects.datefunctions as date_func
from datetime import datetime as dt, timedelta as  td
import numpy as np


class CovidData:
    def __init__(self,country,init_date,days_back,coun_obj):
        self.country =  country
        self.init_date =  init_date
        self.days_back =  days_back
        self.coun_obj = coun_obj
        self.df  =  pd.DataFrame()

    def get_data(self):
        # this function will create data frame for specific country in date range
        # in case all data can't be retrived by one URL query this function will run day by date in defined range and will create one combined dataframe

        try:
            past_dt = self.init_date - td(days=self.days_back)

            url = f"https://api.covid19api.com/country/{self.coun_obj.get_slug_value(self.country)}?from={date_func.return_formatted_date(past_dt)}&to={date_func.return_formatted_date(self.init_date)}"
            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            if response.status_code == 200:
                self.df = self.df.append(pd.DataFrame.from_records(response.json()))
            # check of erro was because of limitation of API response
            elif response.json().get('message','') == 'for performance reasons, please specify a province or a date range up to a week':
                first_num = self.days_back
                count = 0
                for i in reversed(range(self.days_back)):
                    count = count + 1
                    if count % 5 == 0:
                        from_dt = self.init_date - td(days=first_num)
                        to_dt = self.init_date - td(days=i)
                        url = f"https://api.covid19api.com/country/{self.coun_obj.get_slug_value(self.country)}?from={date_func.return_formatted_date(from_dt)}&to={date_func.return_formatted_date(to_dt)}"
                        payload = {}
                        headers = {}
                        print(url)
                        response = requests.request("GET", url, headers=headers, data=payload,timeout=10)
                        if response.status_code == 200:
                            self.df = self.df.append(pd.DataFrame.from_records(response.json()))
                        count = 0
                        first_num = i - 1
            else:
                return ''

        except:
            self.df = pd.DataFrame()
            return ''




    # this function will return max death record for current object
    def get_max_death_record(self):

        if self.df.empty:
            return ""
        shifted = self.df['Deaths'].shift(periods=1,fill_value=0)
        self.df['Death_Dif'] = self.df['Deaths'] - shifted
        self.df.loc[0,['Death_Dif']] = 0
        ret_ind = self.df['Death_Dif'].idxmax()
        return self.df.iloc[[ret_ind]].to_dict()

    # this function will return formatted results for get_max_death_record function
    def get_max_death_record_formatted(self):
        result = self.get_max_death_record()
        if result != '':
            tmp_country = list(result.get('Country').values())[0]
            tmp_method = "newCasesPeak"
            tmp_value = list(result.get('Death_Dif').values())[0]
            tmp_date = list(result.get('Date').values())[0]

            cal_result = {'country':tmp_country,'method':tmp_method,'date':tmp_date,'value':tmp_value}
            return cal_result

    # def get_max_confirmed_record(self):
    #
    #
    #     try:
    #         if self.df.empty:
    #             return ""
    #         shifted = self.df['Confirmed'].shift(periods=1,fill_value=0)
    #         self.df['Confirmed_Dif'] = self.df['Confirmed'] - shifted
    #         self.df.loc[0, ['Confirmed_Dif']] = 0
    #         ret_ind = self.df['Confirmed_Dif'].idxmax()
    #         return self.df.iloc[[ret_ind]].to_dict()
    #     except:
    #         return ""

    def get_max_confirmed_record(self):
        # this function will return max confirmed cases for speciic data set based on country and province
        # since API can retrive data only based on country, this function will slice data frame based on province and will calculate
        # max confirmed cased for each province
        # the result will be max confirmed cased between all province related to specific country

        try:
            if self.df.empty:
                return ""
            self.df['Province'] = np.where(self.df["Province"] == '', self.df['Country'], self.df["Province"])
            province_lst = self.df['Province'].unique()
            final_dict = {}
            max_val = 0
            for el in province_lst:
                rslt_df = self.df.loc[self.df['Province'] == el]
                rslt_df = rslt_df.reset_index(drop=True)
                shifted = rslt_df['Confirmed'].shift(periods=1,fill_value=0)
                rslt_df['Confirmed_Dif'] = rslt_df['Confirmed'] - shifted
                rslt_df.loc[0, ['Confirmed_Dif']] = 0
                ret_ind = rslt_df['Confirmed_Dif'].idxmax()
                tmp_dict = rslt_df.iloc[[ret_ind]].to_dict()
                if list(tmp_dict.get('Confirmed_Dif').values())[0] > max_val:
                    max_val = list(tmp_dict.get('Confirmed_Dif').values())[0]
                    final_dict = tmp_dict
            return final_dict
        except:
            return ""

