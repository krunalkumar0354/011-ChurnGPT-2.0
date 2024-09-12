import requests, os, json, re, time
from datetime import datetime, timedelta

def get_notes_for_company(url, headers, company_id, startT, endT):
  after = 0
  notes = []
  while True:
    payload = {
      "filterGroups": [
        {
          "filters": [
            {
              "propertyName": "associations.company",
              "operator": "EQ",
              "value": company_id
            },
            {
              "propertyName": "hs_timestamp",
              "operator": "GTE",
              "value": startT
            },
            {
              "propertyName": "hs_timestamp",
              "operator": "LTE",
              "value": endT
            }
          ]
        }
      ],
      "properties": ["hs_note_body"],
      "limit": 200,
      "after": after
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
      data = response.json()
      notes.extend(data.get("results", []))
      if "paging" in data and "next" in data["paging"]:
        after = data["paging"]["next"]["after"]
      else:
        break
    else:
      print(f"Error: {response.status_code} - {response.text}")
      break
  return notes

def main(event):
  token = os.getenv("RevOps")
  cId = event.get("inputFields").get("cId")
  closedate = event.get("inputFields").get("ClosedDate")
  url = "https://api.hubapi.com/crm/v3/objects/notes/search"
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
  }
  close_date_dt = datetime.utcfromtimestamp(int(closedate) / 1000)
  start_date_dt = close_date_dt - timedelta(days=120)
  start_timestamp = int(start_date_dt.timestamp() * 1000)
  end_timestamp = int(close_date_dt.timestamp() * 1000)
  notes = []
  time.sleep(3)
  noteswithextradata = get_notes_for_company(url, headers, cId, start_timestamp, end_timestamp)
  for note in noteswithextradata:
    note_body = note["properties"].get("hs_note_body", "No content")
    if type(note_body) != type(None):
      note_body = re.sub(r'<[^>]+>', '', note_body)
      note_body = re.sub(r'http\S+|www\.\S+', '', note_body)
      notes.append(note_body)
  return {
    "outputFields": {
      "CompanyNotes": notes
    }
  }