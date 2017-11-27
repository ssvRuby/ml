import json
import urllib3
import requests
from datetime import date, datetime, timedelta
import time

log_file_name = 'hh.log'
resume_id = '6e1019f2ff040603530039ed1f4b59356a4b71'
current_token = 'UF2U7CSN2C7RCT251529K5BK2C3PQ6VV3MLIP3JJERJEKCL0JJ91DC9U4GJGCRHL'
period = 900 # 900 сек - период обращения к сайту  hh.ru

def print_warning(warning):
    print(warning)


def write_string(filename, message=''):
    with open(filename, 'a') as file:
        file.write(message + '\n')


cio_url = 'https://api.hh.ru/vacancies?text=cio&only_with_salary=false&specialization=1.3&area=1&order_by=publication_time'
sps_url = 'https://api.hh.ru/vacancies?text=&specialization=1.3&area=1&order_by=publication_time'

url_list = []
url_list.append(cio_url)
url_list.append(sps_url)

vacancies = []


def get_vacancies(url_list, vacancies):
    date_from = (date.today() - timedelta(hours=24)).isoformat()

    searches = []
    new_vacancies = []

    for url in url_list:
        for page in range(20):
            try:
                searches.append(requests.get(url + '&page={}&per_page=100&date_from={}'.format(page, date_from)).json())
            except Exception as ex_err:
                write_string(log_file_name, '{} W= Read Vacansies ===> {}'.format(date.today().isoformat(), ex_err))

    try:
        for items in searches:
            for j in items['items']:
                if j['id'] not in vacancies:
                    vacancies.append(j['id'])
                    new_vacancies.append(j['id'])
    except:
        pass

    return new_vacancies


def respond_to_vacancies(vacancies, resume_id, current_token, message=''):
    http = urllib3.PoolManager()

    for vacancy_id in vacancies:
        try:
            r = http.request('POST ', 'https://api.hh.ru/negotiations',
                             headers={'Authorization': 'Bearer {}'.format(current_token),
                                      'Accept': '*/*',
                                      'User-Agent': 'api-test-agent (ssv.ruby@gmail.com)'},
                             fields={'vacancy_id': '{}'.format(vacancy_id),
                                     'resume_id': '{}'.format(resume_id),
                                     'message': '{}'.format(message)
                                     })

            result = 'Vacancy_id: {}, Date: {}, Status: {}, Reason: {}'.format(vacancy_id, r.getheader('Date'),
                                                                               r.status, r.reason)
            write_string(log_file_name, '{} == Respond Vacansies ===> {}'.format(date.today().isoformat(), result))

        except Exception as ex_err:
            write_string(log_file_name, '{} W= Respond Vacansies ===> {}'.format(date.today().isoformat(), ex_err))


while True:
    try:
        write_string(log_file_name, '{} I= Start Vacansies Search '.format(datetime.today().isoformat()))
        new_vacancies = get_vacancies(url_list, vacancies)
        respond_to_vacancies(new_vacancies, resume_id, current_token)
        time.sleep(period)
    except:
        pass








