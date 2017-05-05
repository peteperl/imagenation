import os.path
import tarfile

DATA_FILE = 'inception-2015-12-05.tgz'


def maybe_extract():
  """Download and extract model tar file."""
  dest_directory = 'images'
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
  filename = DATA_FILE
  tarfile.open(filename, 'r:gz').extractall(dest_directory)


if __name__ == '__main__':
  print("Hello")
  maybe_extract()
