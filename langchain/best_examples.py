import argparse
import itertools
import sys
sys.path.append("../.")

from config import Config

def best_input_examples(args):

    with open(f"../{args.config.DATASET_PATH}") as file:
        data = file.readlines()

    data = [list(x[1]) for x in itertools.groupby(data, lambda x: x=='\n') if not x[0]] 
    doc_lens = [len(x) for x in data]

    print([x[0].split('|t|')[0] for x in [data[i] for i in sorted(range(len(doc_lens)), key=doc_lens.__getitem__, reverse=True)[:args.num_examples]]])

    print('hi')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', default='es')
    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"

    configs = Config(args.lang)
    args.config = configs

    args.num_examples = 5

    best_input_examples(args)