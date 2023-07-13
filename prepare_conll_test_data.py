"""
Creating dataset in CoNLL-2003 NER format.
"""
import itertools
import random
import argparse

from config import Config

random.seed(42)

def create_NER_dataset(args):
    bio_ner_data = []

    with open(args.config.TEST_DATASET) as file:
        training_data = file.readlines()

    training_data = [list(x[1]) for x in itertools.groupby(training_data, lambda x: x=='\n') if not x[0]] 

    for data in training_data:
        statement_id = data[0].split('|t|')[0]
        result_entities = []
        test_entities = []
        for relation in data[1:]:
            _,_,result_offset, test_offset, result_entity, test_entity = relation.split('\t')
            result_entities.append((result_entity, result_offset.split('-')))
            test_entities.append((test_entity.strip(), test_offset.split('-')))
        with open(f"{args.config.TEST_TOKEN_DATA}/{statement_id}.tsv") as file:
            tokens = file.readlines()
        
        sentence_splits = [list(x[1]) for x in itertools.groupby(tokens, lambda x: x=='\n') if not x[0]] 
        for sent_num, sentence in enumerate(sentence_splits):
            sentence_data = []
            for token_info in sentence:
                _, token_offsets, token_text = token_info.split('\t')
                token_text = token_text.strip()

                start_offset, end_offset = token_offsets.split('-')

                sentence_data.append((token_text, start_offset, end_offset))
            bio_ner_data.append((statement_id, sent_num, sentence_data))
    return bio_ner_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', default='it')
    args = parser.parse_args()
    configs = Config(args.lang)
    args.config = configs
    bio_ner_data = create_NER_dataset(args)
    with open(f"data_{args.lang}/test_offsets.txt", 'w') as t:
        with open(f"data_{args.lang}/test_tokens.txt", 'w') as x:
            for i, (doc_id, sent_num, sentence) in enumerate(bio_ner_data):
                for token in sentence:
                    t.write('{} {} {} {}\n'.format(doc_id, sent_num, token[1], token[2]))
                    x.write('{}\n'.format(token[0]))
                t.write('\n')
                x.write('\n')

