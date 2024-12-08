import openai
#add import for user db

def location(text):
    country="country" #change this
    api_key="your api key" #change this if you want to add it to a conf file
    def extract_cities(api_key, country, text):
        openai.api_key = api_key
        # Use GPT-4 chat model to identify cities mentioned in the text
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a location master."},
                    {"role": "user", "content": f"List all cities, villages from {country} mentioned in the following text: {text} in JSON format"}
                ]
            )
            cities = response['choices'][0]['message']['content'].strip()
            if cities:
                if cities:
                    return cities
            else:
                return country

        except Exception as e:
            print(f"An error occurred: {e}")
            return country
    return extract_cities(api_key,country,text)