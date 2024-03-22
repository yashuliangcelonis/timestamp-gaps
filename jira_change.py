from jira import JIRA


jira = JIRA(server='https://celonis.atlassian.net/', basic_auth=('y.liang@celonis.com', ""))

issues = jira.search_issues('development[pullrequests].all > 0 AND development[pullrequests].open = 0 AND "Release Team[Select List (multiple choices)]" = "Core Mining Engine - PQL" AND summary ~ "data-model-converter" and status = "Release Approved"')

for issue in issues:
    print(f"Issue Key: {issue.key}")
    print(f"Summary: {issue.fields.summary}")
    print(f"Status: {issue.fields.status.name}")


print("ok")