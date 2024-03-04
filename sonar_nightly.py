from datetime import date
from sonar_util import calculate_dates, get_cache_hit_and_total_time, get_workflow_runs, filter_workflow_runs_by_name

start_date = date(2024, 2, 17)
end_date = date(2024, 2, 28)

# Create a list containing all dates in-between
dates_list = calculate_dates(start_date, end_date)

# get all runs for dates
all_runs = []
for date in dates_list:
    all_runs.extend(get_workflow_runs(date))

nightly_runs = filter_workflow_runs_by_name(all_runs, "Nightly CI")
print(str(len(nightly_runs)) + " Nightly runs found.")

for run in nightly_runs:
    hit_and_total_time = get_cache_hit_and_total_time(run['id'])   
    row = f"Name:{run['name']}, RunID: {run['id']}, Commit:{run['head_sha']}, CreatedAt:{run['created_at']}, Duration:{hit_and_total_time[1]}, CacheHit:{hit_and_total_time[0]}"
    print(row)

