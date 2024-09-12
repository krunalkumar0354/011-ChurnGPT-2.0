import os, requests, time

def main(event):
    token = os.getenv("ChatGPT")
    # Fetch notes and ensure empty notes don't mislead the AI
    cnotes = event.get('inputFields').get('cNotes', '').strip()
    tnotes = event.get('inputFields').get('tNotes', '').strip()
    mnotes = event.get('inputFields').get('mNotes', '').strip()
    enotes = event.get('inputFields').get('eNotes', '').strip()
    name = event.get('inputFields').get('name').strip()

    # Adjusted preText to clarify what the AI should focus on
    preText = f"Summarize in under 250 characters why {name} churned based on the available data. If any notes are missing, it means no information was provided in that section, and you should only consider the provided data."

    # Concatenate notes only if they have content to avoid unnecessary 'no data' text
    notes = []
    if cnotes:
        notes.append(f"Company Notes: {cnotes}")
    if enotes:
        notes.append(f"Email Communication: {enotes}")
    if tnotes:
        notes.append(f"Ticket Notes: {tnotes}")
    if mnotes:
        notes.append(f"Meeting Notes: {mnotes}")
    
    notesText = " ".join(notes) if notes else "No additional information provided."

    # Full final prompt
    finalText = f"{preText} {notesText}. Return only the summary."

    openai_endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Use gpt-4o-mini model and reduce max_tokens to 100
    data = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': finalText}],
        'max_tokens': 100
    }

    # Send the request and handle response
    time.sleep(3)
    response = requests.post(openai_endpoint, headers=headers, json=data)
    conclusion = response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    return {
        "outputFields": {
            "conclusion": conclusion,
        }
    }
