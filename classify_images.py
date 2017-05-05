# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# import os.path
# import re
# from six.moves import urllib

import argparse
import os
import sys
import tarfile

# pylint: disable=line-too-long

TEST = True
FLAGS = None
DOWNLOAD = False
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
IMAGE_DIR = 'images'
IMAGES = []
if not DOWNLOAD: IMAGES = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')]


# pylint: enable=line-too-long


def run_inference_on_image(image):
    print(image)


def maybe_download_and_extract():
    """Download and extract model tar file."""
    dest_directory = FLAGS.model_dir
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                filename, float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()

        filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)


def main():
    if DOWNLOAD:
        maybe_download_and_extract()
        image = (FLAGS.image_file if FLAGS.image_file else
                 os.path.join(FLAGS.model_dir, 'cropped_panda.jpg'))
        run_inference_on_image(image)
    else:
        for image in IMAGES:
            run_inference_on_image(IMAGE_DIR + '/' + image)
    print('DONE')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # classify_image_graph_def.pb:
    #   Binary representation of the GraphDef protocol buffer.
    # imagenet_synset_to_human_label_map.txt:
    #   Map from synset ID to a human readable string.
    # imagenet_2012_challenge_label_map_proto.pbtxt:
    #   Text representation of a protocol buffer mapping a label to synset ID.
    parser.add_argument(
        '--model_dir',
        type=str,
        default='/dev/images',
        help="""\
      Path to classify_image_graph_def.pb,
      imagenet_synset_to_human_label_map.txt, and
      imagenet_2012_challenge_label_map_proto.pbtxt.\
      """
    )
    parser.add_argument(
        '--image_file',
        type=str,
        default='',
        help='Absolute path to image file.'
    )
    parser.add_argument(
        '--num_top_predictions',
        type=int,
        default=5,
        help='Display this many predictions.'
    )
    FLAGS, unparsed = parser.parse_known_args()

    if TEST:
        print('***')
        print(FLAGS)
        print('***')
        print(unparsed)
        print('***')
        print IMAGES
        print('***')
        main()
    else:
        tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
