import requests
import json
import time
import re

# Assembling headers for the HTTP request
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    'referer': 'https://www.campusgroups.com/',
    "cookie": "_ga=GA1.3.2135470572.1676784258; _gid=GA1.3.2006935649.1676784258; CG.SessionID=m5uzqgo0vgb1kr5ragduijux-NAbYz0Mvvaq7y3V7CYYdvzpjRSw%3d; cg_uid=3126080-wUdlP3/3VLwEfZSVoSIUJS0Za0BiFQErZ4awJU5CyCA="
}


def get_info_list(json_data):
    # Initialize dictionaries and lists to store information
    info_dict = {}
    info_list = []
    date_time_list = []

    # Iterate through the JSON data to extract relevant information
    for data in json_data:
        if data['fields'] == "date_separator,date_text,displayType,all_results_hidden,":
            date_time_list.append(data['p1'])
            continue
        # p1 = id, p3 = title, p4 = date and time details
        if data['p1'] != '':
            info_dict['id'] = data['p1']
            info_dict['title'] = data['p3']
            re_obj = re.compile(
                r"<p style='margin:0;'>(.*?), (.*?) (.*?), (.*?)</p><p style='margin:0;'>(.*?) &ndash; (.*?)</p>", re.S)
            result = re_obj.findall(data['p4'])
            info_dict['time'] = result[0]
            info_list.append(info_dict)
            info_dict = {}
    return info_list, date_time_list


def get_info_by_type(data_list, event_type):
    # Initialize lists to store unique times and filtered event information
    unique_times = []
    filtered_list = []

    # Filter the data based on event type
    for event in data_list:
        if event_type == 0 and 'Easton' in event['title']:
            time_range = event['time'][4] + '-' + event['time'][5]
            if time_range not in unique_times:
                unique_times.append(time_range)
            filtered_list.append(event)
        elif event_type == 1 and 'Local' in event['title']:
            time_range = event['time'][4] + '-' + event['time'][5]
            if time_range not in unique_times:
                unique_times.append(time_range)
            filtered_list.append(event)
    return filtered_list


def info_init():
    # Get the current time
    current_time = time.time()
    # Set the number of items to retrieve
    limit = 200
    # Set the search word for the query
    search_word = "shuttle"
    # Construct the URL for the HTTP request
    url = f'https://whattodu.campusgroups.com/mobile_ws/v17/mobile_events_list?range=0&limit={limit}&filter4_contains=OR&filter4_notcontains=OR&order=undefined&search_word={search_word}&{current_time}'

    # Send the GET request and parse the JSON response
    with requests.get(url=url, headers=header) as resp:
        data_list = json.loads(resp.text)
        all_info_list, time_list = get_info_list(data_list)
        return all_info_list


if __name__ == '__main__':
    print(info_init())
