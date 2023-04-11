import openai
import requests
from bs4 import BeautifulSoup
import json
import time

# Set up OpenAI API credentials
openai.api_key = "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"
#Set up VWO API credentials
vwo_account_id = "387486"
vwo_token = "868a42c7ee92603776b4ba9b37dac06020c90fb3b01a0db596de01f85f915633"
headers = {
    "Content-Type": "application/json",
    "Token": vwo_token
}
# print(vwo_token)
# Define function to generate CTA suggestions
def get_cta_suggestions(cta_text):
    # Set up OpenAI API request parameters
    # prompt = (f"Generate suggestions for CTA text '{cta_text}'.\n"
    #           f"Suggestions:")
    # model = "text-davinci-002"
    # temperature = 0.5
    # max_tokens = 5
    # n = 5
    # # Call OpenAI API to generate CTA suggestions
    # response = openai.Completion.create(
    #     engine=model,
    #     prompt=prompt,
    #     temperature=temperature,
    #     max_tokens=max_tokens,
    #     n=n,
    #     stop=None,
    #     )
    # # Extract the generated suggestions from the API response
    # suggestions = [choice.text.strip() for choice in response.choices]
    # return suggestions
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Suggest some alternate to {cta_text}",
        temperature=0.9,
        max_tokens=150,
        # top_p=1,
        # frequency_penalty=0.0,
        # presence_penalty=0.6,
        # stop=[" Human:", " AI:"]
    )
    idea = response.choices[0].text.strip()
    return idea

def create_test():
    # Create VWO test using API
    create_test_url = "https://app.vwo.com/api/v2/accounts/387486/campaigns"
    #print({create_test_url})
    body = {
        "type": "ab",
        "name": "Test created for Demo",
        "urls": [
            {
                "type": "url",
                "value": URL
            }
        ],
        "primaryUrl": URL,
        "goals": [{
            "name": "New goal",
            "type": "visitPage",
            "urls": [
                {
                    "type": "url",
                    "value": URL
                }
            ]
        }],
    }
    return requests.post(create_test_url, headers=headers,data=json.dumps(body))

    

def generate_variation(campaign_id):
    generate_variation_url= f"https://app.vwo.com/api/v2/accounts/{vwo_account_id}/campaigns/{campaign_id}/variations"
    #r = random.randint(0,9)
    variationsData = [
       # {"name": "Control", "changes": {"js": f"document.querySelector('.site-description').textContent = '{cta_text}'"}},
        {
            "variations" : {
                "name": "Variation 1", 
               "changes": {
                   "js": f"document.querySelector('button').textContent = 'text'"
                   }
                }
           # "r": r suggestions[1].text.strip()
        },
        #{"name": "Variation 2", "changes": {"js": f"document.querySelector('.site-description').textContent = '{suggestions[1].text.strip()}'"}},
    ]
    #print(variationsData)
    return requests.post(generate_variation_url, headers=headers,data=json.dumps(variationsData))

# Extract CTA text from website and generate suggestions

URL = "https://mayankjha.wingified.com/test.html"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
cta = soup.find('div', class_='button')
try:
    if cta:
        cta_text = cta.text.strip()
        print("The CTA text is: ", cta_text)

        # Generate suggestions for the CTA text using ChatGPT
        suggestions = get_cta_suggestions(cta_text)
        print("Suggestions:")
        print(suggestions)
        # for suggestion in suggestions:
        #     print("- " + suggestion)

        testCreationResponse = create_test()
        if testCreationResponse.status_code == 201:
            campaign_id = testCreationResponse.json()["_data"]["id"]
            print(f"AB test with ID {campaign_id} created successfully as a draft.")
            # Set up VWO test parameters
            # test_name = f"CTA test created via GPT- {cta_text}"

            time.sleep(1)
            generateVariationResponse = generate_variation(campaign_id)
            if generateVariationResponse.status_code == 201:
                print("Variations generated successfully.")
            else:
                print("Error generating variations.")
                print(generateVariationResponse.json())

        else:
            print("Error creating test.")
            print(testCreationResponse.json())

    else:
        print("No CTA found on the page.")
except:
    print("Other error")