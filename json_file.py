import os, json


def load_file(directory, filename):
  try:
    file_path = '{}/{}'.format(directory, filename)
    with open(file_path, "r") as json_file:
        file_contents = json.load(json_file)
  except FileNotFoundError:
    file_contents = {}
  return file_contents


def write_file(directory, filename, file_contents):
  ensure_dir(directory)
  file_path = '{}/{}'.format(directory, filename)
  with open(file_path, "w") as json_file:
    json.dump(file_contents, json_file)


def ensure_dir(directory):
  os.makedirs(directory, mode=0o777, exist_ok = True)
