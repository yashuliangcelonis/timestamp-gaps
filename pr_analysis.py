import requests
from datetime import datetime
import statistics
import os
import numpy as np

# GitHub API configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

BASE_URL = f'https://api.github.com/search/issues?q='

headers = {
    'Authorization': f'Bearer <your token>',
    'Accept': 'application/vnd.github.v3+json'
}

def get_prs(start_date, end_date):
    query = f'repo:celonis/cpm-query-engine+type:pr+created:2024-01-01..2024-01-31+is:merged+base:main+-author:dependabot[bot]'

    all_prs = []
    page = 1
    while True:
        url = f"{BASE_URL}{query}&page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors
        prs = response.json().get("items", [])

        if not prs:
            break
    
        all_prs.extend(prs)

        if 'next' not in response.links:
            break

        page += 1

    return all_prs

def calculate_pr_lifecycle(prs):
    lifecycles = []
    for pr in prs:
        created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        merged_at = datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
        lifecycle = (merged_at - created_at).total_seconds() / 3600  # in hours
        lifecycles.append(lifecycle)
        # print(f"pr {pr['number']} took {lifecycle:.2f} hours to merge")

    print(f"Number of PRs analyzed: {len(prs)}")
    avg_lifecycle = statistics.mean(lifecycles) if lifecycles else 0
    percentile_90 = np.percentile(lifecycles, 90)
    print(f"Average PR lifecycle: {avg_lifecycle:.0f} hours")
    print(f"90 Percentile PR lifecycle: {percentile_90:.0f} hours")


# Example usage
start_date = "2024-01-01"
end_date = "2024-01-31"

prs = get_prs(start_date, end_date)
avg_lifecycle = calculate_pr_lifecycle(prs)


