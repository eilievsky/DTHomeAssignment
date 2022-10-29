# this class is created to keep list of all countries required for data processing

import requests
import datetime

class Countries:
    def __init__(self):

        self.create_country_dictinary()

    # function to create dictionary of countries based on api response
    # this class hace last refresh date so we can also impkemnet of refresh functionality
    def create_country_dictinary(self):
        url = 'https://api.covid19api.com/countries'
        payload = {}
        headers = {}

        self.last_refresh_date = datetime.datetime.now()

        response = requests.request("GET", url, headers=headers, data=payload)
        tmp_lst = response.json()
        self.country_dict = {}

        for el in tmp_lst:
            self.country_dict[(str(el['Country']).upper())] = el

    # function to retrive Slug value for URL creation based on country name
    def get_slug_value(self,country_name):
        try:
            return self.country_dict[country_name.upper()]['Slug']
        except:
            return('')

    # function to retrive list of countries
    def get_country_list(self):
        return [el['Country'] for el in self.country_dict.values()]







