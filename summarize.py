# Set your API key here (if not using an environment variable)
#openai.api_key = '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'  #Not secure but for demonstration
#from openai 
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

client = OpenAI(api_key='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') #not secure but whatever
# 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 - tony
# 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 - key 2

# Set your API key here (if not using an environment variable)
 #not secure but whatever
@app.route('/summarize', methods=['POST'])
def get_summary(text):
    data = request.json
    text = data.get('text')
    if text == "":
        #print("Please give an input")
        return jsonify({'error': 'Please provide input'}), 400
        return

    try:
        #syntax changes for different gpt models, we're sticking with gpt 3
        response = client.completions.create(#engine="text-davinci-003",
        #response = openai.Completion.create(
            model="text-davinci-003",  # Model you're using
            #model="gpt-4",
            #prompt=f"{text}\n\ntl;dr:",  # Gives the model the input, then says tl;dr afterwards for summary
            prompt=f"{text}\n\n Summarize the former text that I inputted, but then explain how it relates to Texas A&M Univerity.",
            temperature=0.9,  # Controls randomness - cranking up 
            max_tokens=150,  # Max length of response
            top_p=1,  # Diversity of output
            frequency_penalty=1,  # Keeps it succinct
            presence_penalty=0)
    
        summary = response.choices[0].text.strip()

        return jsonify({'summary': summary})
       
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)



#chat gpt assumed this for the connection
#import requests

#url = 'http://127.0.0.1:5000/summarize'
#data = {'text': 'Your long text here'}

#response = requests.post(url, json=data)
#if response.status_code == 200:
#    summary = response.json().get('summary')
#    print(summary)
#else:
#    print("Error:", response.json())

