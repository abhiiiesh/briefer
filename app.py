from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")  # Replace with your OpenAI API key
model_engine = "text-davinci-002"  # Replace with the desired GPT model

def generate_description(prompt):
    prompt = f"Describe {prompt}."
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    description = response.choices[0].text.strip()
    return description

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        company_name = request.form['company_name']
        establishment = request.form['establishment']
        services = request.form['services']
        location = request.form['location']
        prompt = f"Generate 5 grammatically correct with only 150 characters description for business, Business name {company_name} and Establish year as {establishment}  and services by  business are {services} , located in {location}."

        # Generate 5 descriptions
        descriptions = []
        for _ in range(5):
            description = generate_description(prompt)
            descriptions.append(description)

        return render_template('index.html', descriptions=descriptions)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    # Gunicorn server configuration
    host = '0.0.0.0'  # Set the host IP address
    port = int(os.environ.get('PORT', 8080))  # Set the port number

    # Start the Gunicorn server
    from gunicorn.app.base import BaseApplication

    class GunicornApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                      if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': f'{host}:{port}',
        'workers': 4,  # Adjust the number of workers as needed
    }
    GunicornApp(app, options).run()



