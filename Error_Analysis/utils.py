import itertools
import pandas as pd

def get_gold_data(lang):
    with open(f"{lang}-ner/test.txt") as file:
        gold_data = file.readlines()

    gold_data = [list(x[1]) for x in itertools.groupby(gold_data, lambda x: x=='\n') if not x[0]] 

    tokens = []
    gold_labels = []
    for sent in gold_data:
        sent_tokens = []
        sent_labels = []
        for word in sent:
            token, tag = word.split()
            tag = tag.strip()
            assert tag in ["O", "B-TST", "B-RML", "I-TST", "I-RML"]
            sent_tokens.append(token)
            sent_labels.append(tag)
        tokens.append(sent_tokens)
        gold_labels.append(sent_labels)
    
    return tokens, gold_labels

def get_pred_data(lang, model):
    with open(f"{lang}-ner/preds_{model}_test_ner.txt") as file:
        pred_data = file.readlines()
    pred_data = [list(x[1]) for x in itertools.groupby(pred_data, lambda x: x=='\n') if not x[0]] 
    return [[p.strip() for p in pred_sent] for pred_sent in pred_data]

def bio_to_entities(tokens, labels):
    """ Convert BIO tagged tokens into a list of entities. """
    entities = []
    current_entity = []
    current_type = None
    
    for token, label in zip(tokens, labels):
        if label.startswith("B-"):
            if current_entity:
                entities.append((current_type, " ".join(current_entity)))
            current_entity = [token]
            current_type = label[2:]  # Remove the 'B-' part
        elif label.startswith("I-") and current_type is not None:
            if label[2:] == current_type:
                current_entity.append(token)
            else:
                # Handle the case where I- is not consistent with B-
                entities.append((current_type, " ".join(current_entity)))
                current_entity = [token]
                current_type = label[2:]  # Start a new entity type
        else:
            if current_entity:
                entities.append((current_type, " ".join(current_entity)))
                current_entity = []
                current_type = None
    
    # Add the last entity
    if current_entity:
        entities.append((current_type, " ".join(current_entity)))
    
    return entities

def find_missed_entities(tokens_list, true_labels_list, pred_labels_list):
    missed_entities = {}
    
    for tokens, true_labels, pred_labels in zip(tokens_list, true_labels_list, pred_labels_list):
        true_entities = bio_to_entities(tokens, true_labels)
        pred_entities = bio_to_entities(tokens, pred_labels)
        
        for entity_type, entity_value in true_entities:
            if (entity_type, entity_value) not in pred_entities:
                if entity_type not in missed_entities:
                    missed_entities[entity_type] = []
                missed_entities[entity_type].append(entity_value)
    
    return missed_entities

def find_spurious_entities(tokens_list, true_labels_list, pred_labels_list):
    spurious_entities = {}
    
    for tokens, true_labels, pred_labels in zip(tokens_list, true_labels_list, pred_labels_list):
        true_entities = bio_to_entities(tokens, true_labels)
        pred_entities = bio_to_entities(tokens, pred_labels)
        
        # Check for predicted entities not in true entities
        for entity_type, entity_value in pred_entities:
            if (entity_type, entity_value) not in true_entities:
                if entity_type not in spurious_entities:
                    spurious_entities[entity_type] = []
                spurious_entities[entity_type].append(entity_value)
    
    return spurious_entities


def get_relations_from_pubtator(file_name):
    with open(file_name) as file:
        data = file.readlines()
    data = [list(x[1]) for x in itertools.groupby(data, lambda x: x=='\n') if not x[0]]
    gold_relations = []

    for d in data:
        statment_relations = []
        for relation in d[1:]:
            _,_,result_offset, test_offset, result_entity, test_entity = relation.split('\t')
            statment_relations.append((result_entity, test_entity.strip(),
                                       tuple(result_offset.split('-')), 
                                       tuple(test_offset.split('-'))))
        gold_relations.append(statment_relations)   
    
    return gold_relations


def get_gold_relations(lang: str):
    file = f"{lang}-re/gold_test_set.pubtator"
    return get_relations_from_pubtator(file)

def get_pred_relations(lang, model):
    file = f"{lang}-re/{model}_predicted_test_set.pubtator"
    return get_relations_from_pubtator(file)

def get_pred_relations(lang, model):
    file = f"{lang}-re/{model}_predicted_test_set.pubtator"
    return get_relations_from_pubtator(file)

def get_llm_pred_relations(lang, model):
    file = f"{lang}-re/{model}_openai.pubtator"
    return get_relations_from_pubtator(file)

def has_overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2
    return max(start1, start2) < min(end1, end2)

def analyze_relations(true_relations, predicted_relations):
    missed_relations = []
    spurious_relations = []
    partial_relations = []
    
    for true, predicted in zip(true_relations, predicted_relations):
        true_set = set(true)
        predicted_set = set(predicted)
        
        missed = true_set - predicted_set
        spurious = predicted_set - true_set
        
        partial_matches = set()
        
        # Check for partial matches
        for m in missed:
            for p in predicted_set:
                if has_overlap(m[2], p[2]) & has_overlap(m[3], p[3]):
                    partial_matches.add(m)

        missed_relations.append(missed - partial_matches)
        spurious_relations.append(spurious - partial_matches)
        partial_relations.append(partial_matches)
    
    
    missed_relations = [item for sublist in missed_relations for item in sublist]
    spurious_relations = [item for sublist in spurious_relations for item in sublist]
    partial_relations = [item for sublist in partial_relations for item in sublist]

    return missed_relations, spurious_relations, partial_relations

def get_error_type_df(lang):

    gold_relations = get_gold_relations(lang)

    results = {}

    for model in ['mbert', 'xlmroberta', 'biobert', 'mbert_multilingual', 'xlmroberta_multilingual', 'biobert_multilingual']:
        pred_relations = get_pred_relations(lang, model)
        missed, spurious, partial = analyze_relations(gold_relations, pred_relations)
        results[model] = [len(missed), len(spurious), len(partial)]
    
    key_mapping = {
    'mbert': 'mBERT',
    'xlmroberta': 'XLM-RoBERTa',
    'biobert': 'BioBERT',
    'mbert_multilingual': 'mBERT-Multi',
    'xlmroberta_multilingual': 'XLM-RoBERTa-Multi',
    'biobert_multilingual': 'BioBERT-Multi',
    }


    # Rename keys according to the mapping
    for old_key, new_key in key_mapping.items():
        if old_key in results:
            results[new_key] = results.pop(old_key)

    df_results = pd.DataFrame({"Model" : [*results.keys()],
                            "Count" : [*results.values()]
                            }).explode('Count').reset_index(drop=True)
    df_results['Error Type'] = ['Missed', 'Spurious', 'Partial'] * 6

    return df_results

def get_total_num_of_preds(lang, model, llm=False):
    if llm:
        preds = get_llm_pred_relations(lang, model)
    else:
        preds = get_pred_relations(lang, model)
    return len([item for sublist in preds for item in sublist])


def get_total_num_of_relations(lang):
    gold = get_gold_data(lang)
    return len([item for sublist in gold for item in sublist])