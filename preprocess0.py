import numpy as np
import h5py
import re
import sys
import operator
import argparse

def load_bin_vec(fname, vocab):
    """
    Loads 300x1 word vecs from Google (Mikolov) word2vec
    """
    word_vecs = {}
    with open(fname, "rb") as f:
        header = f.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in xrange(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    word.append(ch)
            if word in vocab:
               word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')
            else:
                f.read(binary_len)
    return word_vecs

def line_to_words(line, dataset):
  if dataset == 'SST1' or dataset == 'SST2':
    clean_line = clean_str_sst(line.strip())
  else:
    clean_line = clean_str(line.strip())
  words = clean_line.split(' ')
  words = words[1:]

  return words

def get_vocab(file_list, dataset=''):
  max_sent_len = 0
  word_to_idx = {}
  # Starts at 2 for padding
  idx = 2
  limit = mappedWordsNumber(file_list[0])

  for filename in file_list:
    f = open(filename, "r")
    for line in f:
        if str(line).strip() != "1 *PADDING*":
            words = line_to_words(line, dataset)
            max_sent_len = max(max_sent_len, len(words))
            for word in words:
                if not word in word_to_idx:
                    if idx <= limit + 1:
                        word_to_idx[word] = idx
                        idx += 1
                    else:
                        word_to_idx[word] = 1

    f.close()

  return max_sent_len, word_to_idx

def mappedWordsNumber(train_name):
    with open(train_name) as f:
        size=sum(1 for _ in f)

    return size-1

def load_data(dataset, test_name='', padding=4):

  train_name = dataset + "_word_mapping.txt"
  f_names = []
  if not train_name == '': f_names.append(train_name)
  if not test_name == '': f_names.append(test_name)

  max_sent_len, word_to_idx = get_vocab(f_names, dataset)

  test = []
  test_label = []

  files = []
  data = []
  data_label = []

  if not test_name == '':
    f_test = open(test_name, 'r')
    files.append(f_test)
    data.append(test)
    data_label.append(test_label)

  for d, lbl, f in zip(data, data_label, files):
    for line in f:
        words = line_to_words(line, dataset)
        y = int(line.strip().split()[0]) + 1
        sent = [word_to_idx[word] for word in words]
        # end padding
        if len(sent) < max_sent_len + padding:
          sent.extend([1] * (max_sent_len + padding - len(sent)))
        # start padding
        sent = [1]*padding + sent

        d.append(sent)
        lbl.append(y)

  if not test_name == '':
    f_test.close()

  return word_to_idx, np.array(test, dtype=np.int32), np.array(test_label, dtype=np.int32)

def clean_str(string):
  """
  Tokenization/string cleaning for all datasets except for SST.
  """
  string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
  string = re.sub(r"\'s", " \'s", string)
  string = re.sub(r"\'ve", " \'ve", string)
  string = re.sub(r"n\'t", " n\'t", string)
  string = re.sub(r"\'re", " \'re", string)
  string = re.sub(r"\'d", " \'d", string)
  string = re.sub(r"\'ll", " \'ll", string)
  string = re.sub(r",", " , ", string)
  string = re.sub(r"!", " ! ", string)
  string = re.sub(r"\(", " ( ", string)
  string = re.sub(r"\)", " ) ", string)
  string = re.sub(r"\?", " ? ", string)
  string = re.sub(r"\s{2,}", " ", string)
  return string.strip().lower()

def clean_str_sst(string):
  """
  Tokenization/string cleaning for the SST dataset
  """
  string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
  string = re.sub(r"\s{2,}", " ", string)
  return string.strip().lower()

FILE_PATHS = {"SST1": ("data/stsa.fine.phrases.train",
                  "data/stsa.fine.dev",
                  "data/stsa.fine.test"),
              "SST2": ("data/stsa.binary.phrases.train",
                  "data/stsa.binary.dev",
                  "data/stsa.binary.test"),
              "MR": ("data/rt-polarity.all", "", ""),
              "SUBJ": ("data/subj.all", "", ""),
              "CR": ("data/custrev.all", "", ""),
              "MPQA": ("data/mpqa.all", "", ""),
              "TREC": ("data/TREC.train.all", "", "data/TREC.test.all"),
              }
args = {}

def main():
  global args
  parser = argparse.ArgumentParser(
      description =__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('dataset', help="Data set", type=str)
  parser.add_argument('--test', help="custom test data", type=str, default="")
  parser.add_argument('--padding', help="padding around each sentence", type=int, default=4)
  parser.add_argument('--custom_name', help="name of custom output hdf5 file", type=str, default="custom")
  args = parser.parse_args()
  dataset = args.dataset

  #Train on custom dataset
  test_path = args.test
  dataset = args.custom_name

  # Load data
  word_to_idx, test, test_label = load_data(dataset, test_name=test_path, padding=args.padding)

  filename = dataset + '.hdf5'
  data = []
  with h5py.File(filename, "w") as f:
    f['test'] = test
    f['test_label'] = test_label


if __name__ == '__main__':
  main()
