from jira import JIRA
import json



jira = JIRA(server='https://celonis.atlassian.net/', basic_auth=('y.liang@celonis.com', "<your jira api token>"))

issues = jira.search_issues('development[pullrequests].all > 0 AND development[pullrequests].open = 0 AND "Release Team[Select List (multiple choices)]" = "Core Mining Engine - PQL" AND summary ~ "compute" and status = "Release Approved"')

for issue in issues:
    print("-------------------------")
    print(f"Issue Key: {issue.key}")
    print(f"Summary: {issue.fields.summary}")
    print(f"Status: {issue.fields.status.name}")
    
    # check if there is a merged pr
    json_str = issue.fields.customfield_10000.split("json=")[1][:-1]
    devSummaryJson = json.loads(json_str)
    dev_field_dic = devSummaryJson["cachedValue"]["summary"]
    
    pr_status = dev_field_dic['pullrequest']['overall']['state']
    print(pr_status)
    if pr_status == 'MERGED':
        jira.transition_issue(issue, transition='Release to production')



