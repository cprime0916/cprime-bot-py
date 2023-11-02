import datetime
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')

url = "https://clist.by/api/v3/contest/"

def getcn(hosts):
    contests = []
    for host in hosts:
        params = {
            'username': "cprime",
            "api_key": config["contest"]["key"],
            'upcoming': 'true',
            'host': host
        }

        response = requests.get(url, params=params)
        print(response.text)
        data = response.json()

        if response.status_code == 200 :
            for contest_data in data["objects"]:
                duration = contest_data["duration"] // 60 
                event = contest_data["event"]
                host = contest_data["host"]
                href = contest_data["href"]
                start = contest_data["start"]
                start_utc = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
                start_utc_plus_8 = start_utc + datetime.timedelta(hours=8)

                contests.append({
                    "duration": duration,
                    "event": event,
                    "host": host,
                    "href": href,
                    "start": start_utc_plus_8
                })

    sorted_contests = sorted(contests, key=lambda x: x["start"])
    return sorted_contests