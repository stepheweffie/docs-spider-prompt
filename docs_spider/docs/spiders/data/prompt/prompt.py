import openai
import os
import glob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def analyze_documentation_with_openai(file_pattern, openai_api_key):
    # Initialize the OpenAI client with the API key
    client = openai.OpenAI(api_key=openai_api_key)

    for file_name in glob.glob(file_pattern):
        with open(file_name, 'r') as file:
            file_content = file.read()

            try:
                # Include the file content in your API request
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "I am going to give you some documentation to learn for me."},
                        {"role": "assistant", "content": "Where is the documentation for me?"},
                        {"role": "user", "content": f"{file_content}"}
                    ]
                )
                print(response.choices[0].message.content)
            except openai.APIConnectionError as e:
                print(f"Failed to connect to OpenAI API: {e}")
            except openai.APIError as e:
                print(f"OpenAI API returned an API Error: {e}")
            except openai.RateLimitError as e:
                print(f"OpenAI API request exceeded rate limit: {e}")


# Set your OpenAI API key as an environment variable for security
openai_api_key = os.getenv('OPENAI_API_KEY')

# Replace this with the pattern for your text files
file_pattern = 'prompt*.txt'

analyze_documentation_with_openai(file_pattern, openai_api_key)
