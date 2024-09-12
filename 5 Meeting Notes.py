import os, requests, re, time

def get_meeting_notes(token, ticket_id, base_url, headers):
    url = base_url
    header = headers
    params = {
        'limit': 100
    }
    meeting_notes = []
    has_more = True
    offset = None
    while has_more:
        if offset:
            params['offset'] = offset
        response = requests.get(url, headers = header, params = params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        data = response.json()
        for engagement in data.get('results', []):
            if engagement['engagement']['type'] == 'MEETING':
                meeting_details = {
                    'subject': engagement['metadata'].get('subject', ''),
                    'body': engagement['metadata'].get('body', '')
                }
                meeting_notes.append(meeting_details)
        has_more = data.get('hasMore', False)
        offset = data.get('offset')
    return meeting_notes

def main(event):
  token = os.getenv("RevOps")
  closedate = event.get('inputFields').get('ClosedDate')
  ticket_id = event.get('inputFields').get('hs_ticket_id')
  base_url = f'https://api.hubapi.com/engagements/v1/engagements/associated/ticket/{ticket_id}/paged'
  headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
  }
  time.sleep(3)
  meeting_notes = str(get_meeting_notes(token, ticket_id, base_url, headers))
  meeting_notes = re.sub(r'<[^>]+>', '', meeting_notes)
  return {
    "outputFields": {
      "MeetingNotes": meeting_notes
    }
  }