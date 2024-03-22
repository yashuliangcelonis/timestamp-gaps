from datetime import date
from sonar_util import calculate_dates, calculate_duration, get_cache_hit_and_total_time, get_workflow_runs, filter_workflow_runs_by_name_and_conclusion
import time

start_time = time.time()

start_date = date(2024, 3, 8)
end_date = date(2024, 3, 11)

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
    if not hit_and_total_time:
        hit_and_total_time = []
        hit_and_total_time.append("NA")
        hit_and_total_time.append("NA")
    print(f"RunID:{run['id']}, Commit:{run['head_sha']}, CreatedAt:{run['created_at']}, RunAt:{run['run_started_at']}, Sonar:{hit_and_total_time[0]}, CacheHit:{hit_and_total_time[1]}")

end_time = time.time()
total_runtime = end_time - start_time
print(f"Total runtime of the program is {total_runtime:.6f} seconds")