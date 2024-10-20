import sys
import json
import requests

JIRA_DOMAIN=""
BASIC_TOKEN=""
JIRA_COOKIE=""
HEROCODERS_TOKEN=""

def get_issues_by_filter(filter: str):
  url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/search"

  start_at = 0

  issues = []

  while True:
    payload = json.dumps({
      "startAt": start_at,
      "maxResults": 100,
      "jql": filter,
      "fields": []
    })

    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Basic {BASIC_TOKEN}',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    fetched_issues = [
      issue
      # issue["key"]
      for issue
      in response.json()["issues"]
    ]

    issues += fetched_issues
    start_at += 100

    # return issues
    if len(fetched_issues) == 0:
      return issues

    print(f"listed {len(issues)} issues, going for page {start_at / 100 + 1}")

def add_noreply_and_angelo_as_admin(project_key: str):
  headers = {
    'cookie': JIRA_COOKIE,
    'Content-Type': 'application/json',
    'Authorization': f'Basic {BASIC_TOKEN}',
  }

  possible_admin_role_ids = [
    10002,
    10322,
    10326,
    10874,
    10334,
    10063
  ]

  for admin_role_id in possible_admin_role_ids:
    response = requests.request(
      "POST",
      f"https://{JIRA_DOMAIN}.atlassian.net/rest/projectconfig/latest/roles/{project_key}/{admin_role_id}",
      headers=headers,
      data=json.dumps({
        "users": ["62a22ca95b9785006fd7791b", "632cb1e307a27ebeff1461c5"],
        "groups": [],
      }),
    )

    if response.status_code == 200:
      break

  if response.status_code != 200:
    print(response.text)
    sys.exit(1)

def get_issue_checklist(issue_key: str):
  url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/2/issue/{issue_key}/properties/checklist"

  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {BASIC_TOKEN}',
  }

  response = requests.request("GET", url, headers=headers)

  return response.json()["value"]["items"]

def get_issue_checklist_as_string(issue_key: str):
  url = f"https://whirlpool-lar.atlassian.net/rest/api/2/issue/{issue_key}/properties/checklist"

  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {BASIC_TOKEN}',
  }

  response = requests.request("GET", url, headers=headers)

  return response.json()["value"]["items"]

def add_issue_checklist_backup_comment(issue_key: str):
  issue_checklist = get_issue_checklist_as_string(issue_key)

  headers = {
    'cookie': JIRA_COOKIE,
    'Content-Type': 'application/json',
    'Authorization': f'Basic {BASIC_TOKEN}',
  }

  response = requests.request(
    "POST",
    f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/issue/{issue_key}/comment",
    headers=headers,
    data=json.dumps({
      "body": {
        "version": 1,
        "type": "doc",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "Info",
                "marks": [
                  {
                    "type": "strong"
                  }
                ]
              },
              {
                "type": "text",
                "text": ": Checklist backup"
              },
              {
                "type": "hardBreak"
              },
              {
                "type": "text",
                "text": issue_checklist,
                "marks": [
                  {
                    "type": "code"
                  }
                ]
              }
            ]
          }
        ]
      },
      "visibility": None
    }),
  )

  if response.status_code != 201:
    print(response.text)
    sys.exit(1)


issues = get_issues_by_filter(
  # "checklistItemsCount > 0 and resolved is not EMPTY",
  # "checklistItemsCount > 0",
  "checklistItemsCount > 0 and status in (Done, cancelado, Cancelled) ORDER BY created asc",
)

with open('issues.json', 'w') as f:
  json.dump(issues, f)

# issues = []

# with open('issues.json', 'r') as f:
#   issues = json.load(f)

# project_keys = list(set([
#   issue["key"].split("-")[0]
#   for issue
#   in issues
# ]))

# for project_key in project_keys:
#   print("adding admin for us on " + project_key)
#   add_noreply_and_angelo_as_admin(project_key)

# can_do = True

# for issue in issues:
#   print(issue["key"])

#   if not can_do:
#     # can_do = issue["key"] in ["FL-917"]
#     continue

#   add_issue_checklist_backup_comment(issue["key"])
