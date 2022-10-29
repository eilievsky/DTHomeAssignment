# testing functions. Should be used for development process only
import processobjects.countries as co
import processobjects.coviddata as cov
import datetime as dt
import warnings


def test_one_country_death_data():

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    coun_obj = co.Countries()
    covid_obj = cov.CovidData(country='South Africa',init_date=dt.datetime.now(),days_back=30,coun_obj=coun_obj)
    covid_obj.get_data()
    print(covid_obj.get_max_death_record())

def test_one_country_confirmed_process():

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    coun_obj = co.Countries()

    lst1 = ['france']
    lst2 = []
    for el in lst1:
        print(f"collecting data for {el}")
        covid_obj = cov.CovidData(country=el, init_date=dt.datetime.now(), days_back=30, coun_obj=coun_obj)
        covid_obj.get_data()
        lst2.append(covid_obj.get_max_confirmed_record())
    max_val = 0
    max_val_dict = {}
    for el in lst2:
        if el != '':
            if len(el.keys()) > 0:
                if list(el.get('Confirmed_Dif', 0).values())[0] > max_val:
                    max_val = list(el.get('Confirmed_Dif', 0).values())[0]
                    max_val_dict = el

    tmp_country = list(max_val_dict.get('Country').values())[0]
    tmp_province = list(max_val_dict.get('Province').values())[0]
    tmp_value = list(max_val_dict.get('Confirmed_Dif').values())[0]
    tmp_date = list(max_val_dict.get('Date').values())[0]

    cal_result = {'province': tmp_province, 'country': tmp_country, 'date': tmp_date, 'value': tmp_value}
    print(cal_result)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_one_country_death_data()
    test_one_country_confirmed_process








