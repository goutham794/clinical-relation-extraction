"""
Creating dataset in CoNLL-2003 NER format.
"""
import itertools
import random
import argparse

from config import Config

random.seed(42)

def check_for_entity_match(entity_list, start_offset, end_offset):
    intermediate_state_entity = False
    match_found = False
    matching_entity_number = -1
    for i,test_entity in enumerate(entity_list):
        if start_offset == test_entity[1][0]:
            match_found = True
            matching_entity_number = i
            if end_offset != test_entity[1][1]:
                intermediate_state_entity = True
            break
    return match_found, intermediate_state_entity, matching_entity_number

def create_NER_dataset(args):
    bio_ner_data = []

    with open(args.config.DATASET_PATH) as file:
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
        with open(f"{args.config.TOKEN_DATA_PATH}/{statement_id}.tsv") as file:
            tokens = file.readlines()
        
        sentence_splits = [list(x[1]) for x in itertools.groupby(tokens, lambda x: x=='\n') if not x[0]] 
        intermediate_state_result_entity = False
        intermediate_state_test_entity = False
        for sent_num, sentence in enumerate(sentence_splits):
            sentence_ner_data = []
            for token_info in sentence:
                _, token_offsets, token_text = token_info.split('\t')
                token_text = token_text.strip()

                start_offset, end_offset = token_offsets.split('-')

                if (result_entities == []) & (test_entities == []):
                    sentence_ner_data.append((token_text, "O", start_offset, end_offset))
                    continue


                if intermediate_state_result_entity:
                    if end_offset == result_entities[result_entity_number][1][1]:
                        intermediate_state_result_entity = False
                        result_entities.pop(result_entity_number)
                    sentence_ner_data.append((token_text, "I-RML", start_offset, end_offset))
                    continue

                if intermediate_state_test_entity:
                    if end_offset == test_entities[test_entity_number][1][1]:
                        intermediate_state_test_entity = False
                        test_entities.pop(test_entity_number)
                    sentence_ner_data.append((token_text, "I-TST", start_offset, end_offset))
                    continue
                
                if result_entities != []:
                    match_found, intermediate_state_result_entity, \
                            match_number = check_for_entity_match(result_entities, 
                                                                  start_offset,
                                                                  end_offset)
                    if match_found:
                        sentence_ner_data.append((token_text, "B-RML", start_offset, end_offset))
                        result_entity_number = match_number
                        if not intermediate_state_result_entity:
                            assert result_entity_number != -1
                            result_entities.pop(result_entity_number)
                        continue


                if test_entities != []:
                    match_found, intermediate_state_test_entity, \
                            match_number = check_for_entity_match(test_entities, 
                                                                  start_offset,
                                                                  end_offset)
                    if match_found:
                        sentence_ner_data.append((token_text, "B-TST", start_offset, end_offset))
                        test_entity_number = match_number
                        if not intermediate_state_test_entity:
                            assert test_entity_number != -1
                            test_entities.pop(test_entity_number)
                        continue

                sentence_ner_data.append((token_text, "O", start_offset, end_offset))
            bio_ner_data.append((statement_id, sent_num, sentence_ner_data))
    return bio_ner_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', default='it')
    args = parser.parse_args()
    configs = Config(args.lang)
    args.config = configs
    bio_ner_data = create_NER_dataset(args)
    with open(f"data_{args.lang}/train.txt", 'w') as f1, open(f"data_{args.lang}/valid.txt", "w") as f2:
        with open(f"data_{args.lang}/train_offsets.txt", 'w') as t1, open(f"data_{args.lang}/valid_offsets.txt", "w") as t2:
            with open(f"data_{args.lang}/train_tokens.txt", 'w') as x1, open(f"data_{args.lang}/valid_tokens.txt", "w") as x2:
                for i, (doc_id, sent_num, sentence) in enumerate(bio_ner_data):
                    if doc_id in args.config.VALID_DOC_IDS:
                        f = f2
                        t = t2
                        x = x2
                    else:
                        f = f1
                        t = t1
                        x = x1
                    for token in sentence:
                        f.write('{} {}\n'.format(token[0], token[1]))
                        t.write('{} {} {} {}\n'.format(doc_id, sent_num, token[2], token[3]))
                        x.write('{}\n'.format(token[0]))
                    f.write('\n')
                    t.write('\n')
                    x.write('\n')

