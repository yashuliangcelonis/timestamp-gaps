import datetime
import requests
from zipfile import ZipFile
from io import BytesIO
from datetime import timedelta

headers = {
        "Authorization": f"Bearer <your github dev token>",
        "Accept": "application/vnd.github+json"
}

def calculate_dates(start_date, end_date):
    return [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

def calculate_duration(start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    return str(round((end - start).total_seconds() / 3600, 2))


def get_workflow_runs(date):
    url = f"https://api.github.com/repos/celonis/cpm-query-engine/actions/runs"

    todays_runs = []
    page = 1
    while True:
        print("date/page: "+ str(date) + "/"+ str(page))
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100, "status": "completed", "created": {date}})
        runs = response.json().get("workflow_runs", [])
        if not runs:
            break
        todays_runs.extend(runs)
        page += 1
    return todays_runs

def filter_workflow_runs_by_name_and_conclusion(workflow_runs, target_name, conclusion):
    return [run for run in workflow_runs if run["name"] == target_name and run["conclusion"] == conclusion]

def filter_workflow_runs_by_name(workflow_runs, target_name):
    return [run for run in workflow_runs if run["name"] == target_name]

def get_cache_hit(run_id):
    url = f"https://api.github.com/repos/celonis/cpm-query-engine/actions/runs/{run_id}/logs"

    response = requests.get(url, headers=headers)
    
    #handle zip 
    zipUrl = response.url
    content = requests.get(zipUrl)

    with ZipFile(BytesIO(content.content)) as zip_file:
      try:
        txt_filename = '0_sonarcloud.txt'  
        with zip_file.open(txt_filename) as txt_file:
            for line in txt_file.readlines():
                if b"[INFO] Cache:" in line:
                    return {line.decode('utf-8').strip().split("Cache: ")[1].split(',')[0]}
      except KeyError as e:
        print("ERROR getting sonar log for Run " + str(run_id) + ":" + str(e))
        return "NA"