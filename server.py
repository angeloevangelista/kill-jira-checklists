import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/log_url', methods=['POST'])
def log_url():
    data = request.get_json()

    if 'url' not in data:
      return jsonify({"error": "No URL provided in request body."}), 400

    url = data['url']

    response = requests.request(
      "GET",
      url,
    )


    print(f"Received URL: {url}")
    return jsonify({"page": response.text}), 200

@app.route('/delete_checklist', methods=['POST'])
def delete_checklist():
  data = request.get_json()

  issueKey = data['issueKey']
  token = data['token']
  icToken = data['icToken']
  checklist = data['checklist']

  for item in checklist:
    response = requests.request(
      "DELETE",
      f'https://issue-checklist-free-1.herocoders.com/rest/api/1/{issueKey}/task/{item["id"]}?checklistId=null&issueId={item["issueId"]}&projectId={item["issueId"]}&isIssueDone=true',
      headers={
        "Authorization": f"JWT {token}",
        "x-ic-token": f"JWT {icToken}",
      },
    )

    print(response.status_code)
    print(response.text)

  return jsonify({"ok": True}), 200

@app.route('/delete_completed_checklist', methods=['POST'])
def delete_completed_checklist():
  data = request.get_json()

  issueKey = data['issueKey']
  token = data['token']
  icToken = data['icToken']
  completed_checklist_items = [
    item
    for item
    in data['checklist']
    if 'status' in item and item['status'] == 'done'
  ]

  for item in completed_checklist_items:
    response = requests.request(
      "DELETE",
      f'https://issue-checklist-free-1.herocoders.com/rest/api/1/{issueKey}/task/{item["id"]}?checklistId=null&issueId={item["issueId"]}&projectId={item["issueId"]}&isIssueDone=true',
      headers={
        "Authorization": f"JWT {token}",
        "x-ic-token": f"JWT {icToken}",
      },
    )

    print(response.status_code)
    print(response.text)


  return jsonify({"ok": True}), 200

if __name__ == '__main__':
  app.run(debug=True, port=3333)
