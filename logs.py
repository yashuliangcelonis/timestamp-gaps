import os
import requests
from zipfile import ZipFile
from io import BytesIO
import datetime



headers = {
        "Authorization": f"Bearer <your token>",
        "Accept": "application/vnd.github+json"
}

def get_all_workflow_runs():
    url = f"https://api.github.com/repos/celonis/cpm-query-engine/actions/runs"

    all_runs = []
    page = 1
    while True:
        print("page: "+ str(page))
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100, "status": "completed", "created": "2024-02-14"})
        runs = response.json().get("workflow_runs", [])
        if not runs:
            break
        all_runs.extend(runs)
        page += 1
    return all_runs

def filter_workflow_runs_by_name_and_conclusion(workflow_runs, target_name, conclusion):
    return [run for run in workflow_runs if run["name"] == target_name and run['conclusion'] == conclusion]

def get_cache_hit(run_id):
    url = f"https://api.github.com/repos/celonis/cpm-query-engine/actions/runs/{run_id}/logs"

    response = requests.get(url, headers=headers)
    
    #handle zip 
    zipUrl = response.url
    content = requests.get(zipUrl)

    with ZipFile(BytesIO(content.content)) as zip_file:
      txt_filename = '0_sonarcloud.txt'  
      with zip_file.open(txt_filename) as txt_file:
          for line in txt_file.readlines():
              if b"[INFO] Cache:" in line:
                        return {line.decode('utf-8').strip().split("Cache: ")[1].split(',')[0]}

def calculate_duration(start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    return str(round((end - start).total_seconds() / 3600, 2))

all_runs = get_all_workflow_runs()
pr_runs = filter_workflow_runs_by_name_and_conclusion(all_runs, "Pull Request CI", "success")

for run in pr_runs:
    string_cache_hit = get_cache_hit(run['id'])
    string_duration = calculate_duration(run['created_at'], run['updated_at'])
    print(f"Name: {run['name']}, Run ID: {run['id']}, Status: {run['conclusion']}, Created At: {run['created_at']}, Duration: {string_duration}H, Cache Hit: {string_cache_hit}")
