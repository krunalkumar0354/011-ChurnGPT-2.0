import os, requests, time

def main(event):
    token = os.getenv("ChatGPT")
    reason = event.get('inputFields').get('churn_reason', '')
    summary = event.get('inputFields').get('conclusion', '')
    
    # Simplified prompt for better efficiency
    finalText = f"Is the churn reason '{reason}' correct? Review this summary: {summary}. Answer 'yes' or 'no' with a brief explanation."

    openai_endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Use gpt-4o-mini model
    data = {
        'model': 'gpt-4o-mini',  # Optimized for this model
        'messages': [{'role': 'user', 'content': finalText}],
        'max_tokens': 100
    }

    # Send the request and handle response
    time.sleep(3)
    response = requests.post(openai_endpoint, headers=headers, json=data)
    correctness = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

    return {
        "outputFields": {
            "Correctness": correctness
        }
    }
