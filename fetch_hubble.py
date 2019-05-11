import os, requests, json_file
from dotenv import load_dotenv


def get_image(file_path, url):
  response = requests.get(url)
  if response.ok:
      with open(file_path, 'wb') as file:
          file.write(response.content)


def fetch_hubble_collection_image_ides(collection_name):
    response = requests.get("http://hubblesite.org/api/v3/images?page=all&collection_name={}".format(collection_name))
    images_id = []
    if response.ok:
        for collection_name in  response.json():
            images_id.append(collection_name['id'])

    return images_id


def get_hubble_images(directory, json_filename, image_ides):
    for image_id in image_ides:
        hubble_urls = fetch_hubble_images(directory, json_filename, image_id)

        if hubble_urls:
            url = hubble_urls[-1]
            small_filename = url.split('/')[-1]

            file_path = "{}/{}_{}".format(directory, image_id, small_filename)
            get_image(file_path, url)


def fetch_hubble_images(directory, json_filename, image_id):
    response = requests.get("http://hubblesite.org/api/v3/image/{}".format(image_id))
    urls = []
    if response.ok:
         description = response.json()['name']

         files_info = json_file.load_file(directory, json_filename)
         for url in response.json()['image_files']:
             urls.append(url['file_url'])
             small_filename = url['file_url'].split('/')[-1]
             filename = "{}_{}".format(image_id, small_filename)

             if filename not in files_info:
                 files_info[filename] = {
                        "caption": description,
                        "posted": False
                 }
             json_file.write_file(directory, json_filename, files_info)
    return urls


def main():
  load_dotenv()

  directory = os.getenv("DIRECTORY")
  json_filename = os.getenv("JSON_FILENAME")

  # Коллекции: "holiday_cards", "wallpaper", "spacecraft", "news", "printshop", "stsci_gallery"

  image_ides = fetch_hubble_collection_image_ides("stsci_gallery")
  get_hubble_images(directory, json_filename, image_ides)


if __name__ == "__main__":
  main()
