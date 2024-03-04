from datetime import date
from sonar_util import calculate_dates, calculate_duration, get_cache_hit_and_total_time, get_workflow_runs, filter_workflow_runs_by_name_and_conclusion

start_date = date(2024, 2, 17)
end_date = date(2024, 2, 18)

# Create a list containing all dates in-between
dates_list = calculate_dates(start_date, end_date)

# get all runs for dates
all_runs = []
for date in dates_list:
    all_runs.extend(get_workflow_runs(date))

pr_runs = filter_workflow_runs_by_name_and_conclusion(all_runs, "Pull Request CI", "success")
print(str(len(pr_runs)) + " PR runs found.")

for run in pr_runs:
    hit_and_total_time = get_cache_hit_and_total_time(run['id'])
    string_duration = calculate_duration(run['created_at'], run['updated_at'])
    print(f"RunID:{run['id']}, Commit:{run['head_sha']}, CreatedAt:{run['created_at']}, Duration:{string_duration}H, Sonar:{hit_and_total_time[1]}, CacheHit:{hit_and_total_time[0]}")
