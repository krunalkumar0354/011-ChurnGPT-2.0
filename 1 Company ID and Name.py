import requests,os, time

def main(event):
  token = os.getenv("RevOps")
  closedate = event.get("inputFields").get("closed_date")
  ticketid = event.get("inputFields").get("hs_ticket_id")
  url = f"https://api.hubapi.com/crm/v4/objects/tickets/{ticketid}/associations/company"
  headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
  }
  cId = None
  name = None
  time.sleep(3)
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    company = response.json()
    if company.get("results"):
      for i in company["results"]:
        cId = i['toObjectId']
        url = f"https://api.hubapi.com/crm/v4/objects/companies/{cId}"
        response = requests.get(url, headers=headers)
        company_details = response.json()
        company_name = company_details.get("properties", {}).get("name")
        if company_name:
          name = company_name
    else:
      cId = None
      name = None
  else:
    cId = None
    name = None
  return {
    "outputFields": {
      "AssociatedCompanyID": cId,
      "AssociatedCompanyName": name,
      "ClosedDate": closedate
    }
  }