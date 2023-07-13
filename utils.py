import itertools
from collections import Counter
import re
import subprocess

import config_old


def create_tokens_list_from_file(filename):
    with open(filename) as f:
        data = f.readlines()
        data = [[y.strip() for y in list(x[1])] for x in itertools.groupby(data, lambda x: x=='\n') if not x[0]] 
        return data

def save_predictions_to_file(preds, lang, filename):
    with open(f'results_{lang}/{filename}', 'w') as f:
        for sent_preds in preds:
            for pred in sent_preds:
                f.write(f'{pred}\n')
            f.write('\n')


def get_entity_spans(tag_list, entity_type):
    entity_spans = []
    start_offset = None
    
    for i, tag in enumerate(tag_list):
        if start_offset is not None:
            if tag != f"I-{entity_type}":
                entity_spans.append((start_offset, i-1))
                start_offset = None

        if tag == f"B-{entity_type}":
            start_offset = i
    
    if start_offset is not None:
        entity_spans.append((start_offset, len(tag_list)-1))
    
    return entity_spans


def get_predicted_entity_offsets(predictions_file, offsets_file):
    entity_offsets = []

    with open(predictions_file) as f1, open(offsets_file) as f2:
        predictions = f1.readlines()
        offsets = f2.readlines()
    predictions_sentence_grouped  = [list(x[1]) for x in itertools.groupby(predictions, lambda x: x=='\n') if not x[0]] 
    offsets_sentence_grouped  = [list(x[1]) for x in itertools.groupby(offsets, lambda x: x=='\n') if not x[0]] 

    for sent_preds, sent_offsets in zip(predictions_sentence_grouped, offsets_sentence_grouped):
        sent_preds = [p.strip() for p  in sent_preds]
        sent_offsets = [tuple(o.strip().split()) for o in sent_offsets]
        num_rml_entities = Counter(sent_preds)['B-RML']
        num_tst_entities = Counter(sent_preds)['B-TST']
        result_entity_spans = get_entity_spans(sent_preds, 'RML')
        test_entity_spans = get_entity_spans(sent_preds, 'TST')
        assert len(result_entity_spans) == num_rml_entities
        assert len(test_entity_spans) == num_tst_entities
        sent_rml_entity_offsets = [(sent_offsets[i][2], sent_offsets[j][3]) for i,j in result_entity_spans]
        sent_tst_entity_offsets = [(sent_offsets[i][2], sent_offsets[j][3]) for i,j in test_entity_spans]

        entity_offsets.append((sent_rml_entity_offsets, sent_tst_entity_offsets))
        
    return entity_offsets




def save_predicted_pubtator(df_relations, lang, filename, 
                            dataset_path):

    with open(f"{dataset_path}") as file:
        training_data = file.readlines()

    training_data = [list(x[1]) for x in itertools.groupby(training_data, lambda x: x=='\n') if not x[0]]

    result_entity_regex = f"{re.escape(config_old.RESULT_ENTITY_MARKER)}(.*?){re.escape(config_old.RESULT_ENTITY_MARKER)}"
    test_entity_regex = f"{re.escape(config_old.TEST_ENTITY_MARKER)}(.*?){re.escape(config_old.TEST_ENTITY_MARKER)}"
    with open(f"results_{lang}/{filename}", 'w') as f:
        for data in training_data:
            statement_id = data[0].split('|t|')[0]
            f.write(data[0])
            relations = df_relations[df_relations.doc_id == int(statement_id)]
            for relation in relations.itertuples():
                rml_entity = re.findall(result_entity_regex, relation.text)[0]
                test_entity = re.findall(test_entity_regex, relation.text)[0]
                f.write(f"{relation.doc_id}\tREL\t{relation.rml_s}-{relation.rml_e}\t{relation.tst_s}-{relation.tst_e}\t{rml_entity}\t{test_entity}\n")
            f.write('\n')


def get_pubtator_scores(lang, model, split):
    shell_script = "./eval_relation.sh"

    arg1 = "PubTator"
    arg2 = f"../data_{lang}/gold_{split}_set.pubtator"
    arg3 = f"../results_{lang}/{model}_predicted_{split}_set.pubtator"

    directory = "BC5CDR_Evaluation-0.0.3/"

    result = subprocess.run(['/bin/sh', shell_script, arg1, arg2, arg3], capture_output=True,
                text=True, cwd=directory )
    
    return {x.split(':')[0]:x.split(':')[1] for x in result.stdout.split('\n')[:-1]}


def find_comma_not_decimal(s):
    for i, char in enumerate(s):
        if char == ",":
            before = s[i - 1] if i - 1 >= 0 else None
            after = s[i + 1] if i + 1 < len(s) else None
            
            if not (before.isdigit() and after.isdigit()):
                return True
                
    return False



def classify_relation(text):
    indexes = [text.find("[RML]"), text.find("[TST]")]
    indexes.sort()
    return not find_comma_not_decimal(text[indexes[0]: indexes[1]])