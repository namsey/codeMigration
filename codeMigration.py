import asyncio
import json
import aiohttp
import os


async def main():
    api_key = os.environ.get('API_KEY')  # Get API key from environment variable
    if api_key is None:
        raise ValueError('API_KEY environment variable not set.')
    input_directory = r"C:\Users\176381\dotNet\FRAMEWORK"
    output_directory = r"C:\Users\176381\New folder"
    for root, dirs, files in os.walk(input_directory):
        for directory in dirs:
            # Create corresponding output directory in the output_directory
            output_subdirectory = os.path.join(output_directory,
                                               os.path.relpath(os.path.join(root, directory), input_directory))
            os.makedirs(output_subdirectory, exist_ok=True)

            for filename in os.listdir(os.path.join(root, directory)):
                # Get the complete file path by joining the input directory path with the file name
                input_file = os.path.join(root, directory, filename)
                print(input_file)
                if os.path.isfile(input_file):
                    # Create output file path by replacing file extension
                    #                    output_file = os.path.join(output_subdirectory, os.path.splitext(filename)[0] + ".py")
                    output_file = os.path.join(output_subdirectory,
                                               os.path.splitext(filename)[0] + os.path.splitext(filename)[1])
                    with open(input_file) as f:
                        lines = f.readlines()
                        formatted_str = ''.join(lines).replace('\r\n', '\\n').replace('\r', '').replace('\n', '\\\\n ')
                        input_str = "convert this web application asp.net framework v4.0 to ASP.NET Core Razor Pages v7.0" + r"\n" + r"\n" + formatted_str
                        await process_input(input_str, api_key, output_file)


async def process_input(input_str, api_key, output_file):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": input_str,
            "max_tokens": 3000,
            "temperature": 0.7,
        }
        async with session.post(
                "https://api.openai.com/v1/engines/text-davinci-003/completions",
                headers=headers,
                data=json.dumps(data),
        ) as response:
            json_data = await response.json()
            print(json_data)
            output_text = json_data["choices"][0]["text"] + "\n"
            output_text = output_text.replace('\\n', '\n').replace('\\', '')

            with open(output_file, 'w') as f:  # Save output to file
                f.write(output_text)


if __name__ == "__main__":
    asyncio.run(main())
