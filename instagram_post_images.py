import os, time, json_file
from dotenv import load_dotenv
from instabot import Bot


def posting_images(login, password, directory, json_filename):
  bot = Bot()
  bot.login(username=login, password=password)

  pics = os.listdir("{}".format(directory))

  files_info = json_file.load_file(directory, json_filename)

  for pic in pics:
    filename = pic.split('\\')[-1]

    if filename not in files_info:
      continue

    if files_info[filename]["posted"]:
      continue

    caption = files_info[filename]["caption"]

    file_path = "{}/{}".format(directory, pic)
    bot.upload_photo(file_path, caption=caption)

    if bot.api.last_response.status_code != 200:
      break

    files_info[filename]["posted"] = True
    json_file.write_file(directory, json_filename, files_info)

    time.sleep(60)
  bot.logout()


def main():
  load_dotenv()

  login = os.getenv("LOGIN")
  password = os.getenv("PASSWORD")
  directory = os.getenv("DIRECTORY")
  json_filename = os.getenv("JSON_FILENAME")

  posting_images(login, password, directory, json_filename)


if __name__ == "__main__":
  main()
