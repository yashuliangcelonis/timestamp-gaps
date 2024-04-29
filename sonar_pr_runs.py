# how many pr runs per day
# and average per day

from datetime import date
from sonar_util import calculate_dates, get_workflow_runs, filter_workflow_runs_by_name_and_conclusion
import time

start_time = time.time()

start_date = date(2024, 3, 1)
end_date = date(2024, 4, 29)

# Create a list containing all dates in-between
dates_list = calculate_dates(start_date, end_date)

# get all runs for dates
total_runs = 0
days = 0
for date in dates_list:
    all_runs_daily = get_workflow_runs(date)
    pr_runs = filter_workflow_runs_by_name_and_conclusion(all_runs_daily, "Pull Request CI", "success")
    pr_run_count = len(pr_runs)
    print(f"{date}:{pr_run_count}")

    if(pr_run_count > 5):
        total_runs = total_runs + pr_run_count
        days = days + 1


print(f"total days: {days} - total runs: {total_runs}- avg runs: {total_runs/days}")
    
