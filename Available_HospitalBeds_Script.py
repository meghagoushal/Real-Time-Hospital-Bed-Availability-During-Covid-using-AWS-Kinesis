import json
import csv
import calendar
import time
from urllib.request import urlopen
from apscheduler.schedulers.blocking import BlockingScheduler

def create_file(file_name, jsonObj):
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    file_name = file_name + str(ts) + '.csv'
    data_file = open(file_name, 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for emp in jsonObj:
        #print(bed_data[emp].values())
        if count == 0:
            keys = ['name']
            keys.extend(list(jsonObj[emp].keys()))
            csv_writer.writerow(keys)
            count += 1

        # Writing data of CSV file

        if emp == 'All':
            continue
        values = [emp]
        values.extend(jsonObj[emp].values())
        values = clean_data(values)
        csv_writer.writerow(values)

    print('file: ', file_name)
    data_file.close()


def clean_data(list_data):
    new_list = []
    for col in list_data:
        new_string = ''.join(char for char in str(col) if char.isalnum() or char == ' ')
        new_list.append(str(new_string))
    return new_list

def fetch_data():
    url = "https://coronabeds.jantasamvad.org/covid-info.js"
    page = urlopen(url)
    html_bytes = page.read()
    data = html_bytes.decode("utf-8")
    obj = data[data.find('{') : data.rfind('}')+1]
    jsonObj = json.loads(obj)
    create_file('beds_data_', jsonObj['beds'])
    create_file('oxygen_beds_', jsonObj['oxygen_beds'])
    create_file('covid_icu_beds_', jsonObj['covid_icu_beds'])
    create_file('icu_beds_without_ventilator_', jsonObj['icu_beds_without_ventilator'])
    create_file('noncovid_icu_beds_', jsonObj['noncovid_icu_beds'])
    create_file('oxygen_left_for_', jsonObj['oxygen_left_for'])
    create_file('ventilators_', jsonObj['ventilators'])

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_data, 'interval', seconds=5)
    scheduler.start()
