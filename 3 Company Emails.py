import requests, os, json, re, time
from datetime import datetime, timedelta

def get_emails_for_company(url, headers, company_id, startT, endT):
    after = 0
    emails = []
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
                            "propertyName": "engagement.type",
                            "operator": "EQ",
                            "value": "EMAIL"
                        },
                        {
                            "propertyName": "engagement.timestamp",
                            "operator": "GTE",
                            "value": startT
                        },
                        {
                            "propertyName": "engagement.timestamp",
                            "operator": "LTE",
                            "value": endT
                        }
                    ]
                }
            ],
            "properties": ["hs_email_body"],
            "limit": 200,
            "after": after
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            emails.extend(data.get("results", []))
            if "paging" in data and "next" in data["paging"]:
                after = data["paging"]["next"]["after"]
            else:
                break
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break
    return emails

def main(event):
    token = os.getenv("RevOps")
    cId = event.get("inputFields").get("cId")
    closedate = event.get("inputFields").get("ClosedDate")
    url = "https://api.hubapi.com/crm/v3/objects/engagements/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    close_date_dt = datetime.utcfromtimestamp(int(closedate) / 1000)
    start_date_dt = close_date_dt - timedelta(days=120)
    start_timestamp = int(start_date_dt.timestamp() * 1000)
    end_timestamp = int(close_date_dt.timestamp() * 1000)
    emails = []
    time.sleep(3)
    email_engagements = get_emails_for_company(url, headers, cId, start_timestamp, end_timestamp)
    finalemail = ""
    for email in email_engagements:
        eid = email["id"]
        response = requests.get(f"https://api.hubapi.com/engagements/v1/engagements/{eid}", headers=headers)
        engagement_details = response.json()
        metadata = engagement_details.get("metadata", {})
        subject = metadata.get("subject", "")
        email_html = metadata.get("html", "")
        finalemail = subject + email_html
        finalemail = re.sub('<.*?>','',finalemail)
        finalemail = finalemail.replace('\n','')
        emails.append(finalemail)
    return {
        "outputFields": {
            "CompanyEmails": emails
        }
    }
