import requests, json_file, os
from dotenv import load_dotenv


def get_image(file_path, url):
    response = requests.get(url)
    if response.ok:
        with open(file_path, 'wb') as file:
            file.write(response.content)


def get_spacex_images(directory, urls):
    for url in urls:
        filename = url.split('/')[-1]

        file_path = "{}/{}".format(directory, filename)
        get_image(file_path, url)


def fetch_spacex_last_launch(directory, json_filename):
    response = requests.get("https://api.spacexdata.com/v3/launches/latest")
    if response.ok:
        description = 'SpaceX {} Mission'.format(response.json()['mission_name'])
        urls = []
        files_info = json_file.load_file(directory, json_filename)
        for url in response.json()['links']['flickr_images']:
            filename = url.split('/')[-1]
            if filename not in files_info:
                files_info[filename] = {
                    "caption": description,
                    "posted": False
                }
        json_file.write_file(directory, json_filename, files_info)

        return response.json()['links']['flickr_images']
    else:
        return None


def main():
    load_dotenv()

    directory = os.getenv("DIRECTORY")
    json_filename = os.getenv("JSON_FILENAME")

    spacex_urls = fetch_spacex_last_launch(directory, json_filename)

    if spacex_urls:
        get_spacex_images(directory, spacex_urls)


if __name__ == "__main__":
  main()
