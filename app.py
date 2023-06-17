from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
model_engine = "text-davinci-002"

def generate_description(prompt):
    prompt = f"Describe {prompt}."
    try:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=700,
            n=1,
            stop=None,
            temperature=0.5,
        )
        description = response.choices[0].text.strip()
        return description
    except Exception as e:
        # Handle OpenAI API errors
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        company_name = request.form['company_name']
        establishment = request.form['establishment']
        services = request.form['services']
        location = request.form['location']
        prompt = f"Generate 5 grammatically correct 300-character attractive descriptions for the business. Business name: {company_name}, Established in: {establishment}, Services: {services}, Location: {location}."

        descriptions = []
        description = generate_description(prompt)
        descriptions.append(description)


        return render_template('index.html', descriptions=descriptions)
    else:
        return render_template('index.html')

@app.errorhandler(Exception)
def handle_error(e):
    # Return JSON response for any unhandled exception
    response = jsonify(error=str(e))
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)




