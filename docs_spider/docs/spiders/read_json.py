import json

# Replace this with your JSON file path
json_file_path = 'output.json'


def print_unique_keys(file_path):
    try:
        # Open and read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Check if the data is a list of dictionaries
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            unique_keys = set()
            for item in data:
                unique_keys.update(item.keys())

            # Print the unique keys
            print("Unique keys found in the JSON file:")
            for key in unique_keys:
                print(key)
        else:
            print("The JSON file does not contain a list of dictionaries.")
    except Exception as e:
        print(f"An error occurred: {e}")


print_unique_keys(json_file_path)


def split_prompts_to_files(file_path, max_length=4096):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    prompt_number = 1
    current_length = 0
    prompt = ""

    for item in data:
        text = item.get('text', '')
        code = item.get('code', '')
        content = text if text else code  # Use text if available, otherwise use code
        addition_length = len(content) + 2  # Add 2 for the newlines

        # Check if adding this content would exceed the limit
        if current_length + addition_length > max_length and current_length > 0:
            # Save the current prompt to a file
            file_name = f'prompt{prompt_number}.txt'
            with open(file_name, 'w') as prompt_file:
                prompt_file.write(prompt.strip())

            # Start a new prompt
            prompt_number += 1
            prompt = content + "\n\n"
            current_length = addition_length
        else:
            prompt += content + "\n\n"
            current_length += addition_length

    # Write the last prompt if there's remaining content
    if prompt:
        file_name = f'prompt{prompt_number}.txt'
        with open(file_name, 'w') as prompt_file:
            prompt_file.write(prompt.strip())


# Replace this with your JSON file path
json_file_path = 'output.json'
split_prompts_to_files(json_file_path)



