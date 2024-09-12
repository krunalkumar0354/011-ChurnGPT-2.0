import os, requests

def main(event):
    token = os.getenv("ChatGPT")
    correctness = event.get('inputFields', {}).get('Correctness', '')

    # Concise list of churn reasons
    churn_reasons = "Company Shut Down, Lack of Funding, Pricing Issues, Service Issues, ICP Misfit, Hired In-House Team, Moved to NetSuite, Moved to Competitor, Zeni's Decision, Company Sold, Controller Issue"
    
    # Streamlined and concise prompt
    final_prompt = f"Based on: '{correctness}', pick one churn reason from: {churn_reasons}. If undetermined, respond with 'Undetermined'"

    openai_endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Efficient payload with a smaller max_tokens
    data = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': final_prompt}],
        'max_tokens': 50
    }

    # Send the request and handle response
    response = requests.post(openai_endpoint, headers=headers, json=data)
    reason = response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    return {
        "outputFields": {
            "RecommendedChurnReason": reason
        }
    }
