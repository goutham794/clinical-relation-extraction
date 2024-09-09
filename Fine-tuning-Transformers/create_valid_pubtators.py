import argparse
import itertools

from config import Config

def save_valid_pubtators(args):

    with open(args.config.DATASET_PATH) as f1:
        training_data = f1.readlines()
        training_data = [list(x[1]) for x in itertools.groupby(training_data, lambda x: x=='\n') if not x[0]] 
        with open(f"data_{args.lang}/gold_valid_set.pubtator", 'w') as f2:
            for doc in training_data:
                if doc[0].split('|t|')[0] not in args.config.VALID_DOC_IDS:
                    continue
                for line in doc:
                    f2.write(line)
                f2.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', default='it')

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    configs = Config(args.lang)
    args.config = configs
    save_valid_pubtators(args)