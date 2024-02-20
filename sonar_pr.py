from datetime import date
from sonar_util import calculate_dates, calculate_duration, get_cache_hit, get_workflow_runs, filter_workflow_runs_by_name_and_conclusion

start_date = date(2024, 2, 19)
end_date = date(2024, 2, 20)

# Create a list containing all dates in-between
dates_list = calculate_dates(start_date, end_date)

# get all runs for dates
all_runs = []
for date in dates_list:
    all_runs.extend(get_workflow_runs(date))

pr_runs = filter_workflow_runs_by_name_and_conclusion(all_runs, "Pull Request CI", "success")

for run in pr_runs:
    string_cache_hit = get_cache_hit(run['id'])
    string_duration = calculate_duration(run['created_at'], run['updated_at'])
    print(f"Name:{run['name']}, RunID:{run['id']}, Commit:{run['head_sha']}, Status:{run['conclusion']}, CreatedAt:{run['created_at']}, Duration:{string_duration}H, CacheHit:{string_cache_hit}")
