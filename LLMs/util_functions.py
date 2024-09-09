import itertools
import re

def get_examples_for_prompt(dataset_path, few_shot_doc_ids):
    """
    Get example clincal statements to be used in the few-shot prompt.
    """
    with open(f"../{dataset_path}") as file:
        data = file.readlines()

    data = [list(x[1]) for x in itertools.groupby(data, lambda x: x=='\n') if not x[0]] 
    
    examples_in_prompt = []

    for doc in data:
        doc_id = doc[0].split('|t|')[0]
        if doc_id not in few_shot_doc_ids:
            continue
        text_and_output = {}
        text_and_output['Text'] = doc[0].split('|t|')[1].strip()
        text_and_output['Output'] = ""

        for relation in doc[1:]:
            _,_,_, _, result_entity, test_entity = relation.split('\t')
            text_and_output['Output'] += f"{result_entity} | {test_entity.strip()}\n"

        examples_in_prompt.append(text_and_output)
    
    return examples_in_prompt


def read_clinical_docs(dataset_path):
    docs = []
    with open(f"../{dataset_path}") as file:
        data = file.readlines()
    data = [list(x[1]) for x in itertools.groupby(data, lambda x: x=='\n') if not x[0]] 
    for doc in data:
        statement_id = doc[0].split('|t|')[0]
        docs.append((statement_id,  doc[0].split('|t|')[1].strip()))
    return docs

def check_rml_tst_same_sentence(rml_indexes, tst_indexes, doc_id, tokens_path):
    """
    Returns indexes of rml and test entity that belong to same sentence or `None` otherwise.
    """
    with open(f"../{tokens_path}/{doc_id}.tsv") as file:
        tokens = file.readlines()
    sentence_splits = [list(x[1]) for x in itertools.groupby(tokens, lambda x: x=='\n') if not x[0]] 

    for r_i, t_i in zip(rml_indexes, tst_indexes):
        for sentence in sentence_splits:
            if (r_i[0] <= int(sentence[-1].strip().split('\t')[1].split('-')[0])) and (t_i[0] <= int(sentence[-1].strip().split('\t')[1].split('-')[0])) \
                and (r_i[0] >= int(sentence[0].strip().split('\t')[1].split('-')[0])) and (t_i[0] >= int(sentence[0].strip().split('\t')[1].split('-')[0])):
                start_offsets, end_offsets = [], []
                for token in sentence:
                    start_offsets.append(token.split('\t')[1].split('-')[0])
                    end_offsets.append(token.split('\t')[1].split('-')[1])
                try:

                    assert str(r_i[0]) in start_offsets
                    assert str(r_i[1]) in end_offsets
                    assert str(t_i[0]) in start_offsets
                    assert str(t_i[1]) in end_offsets
                    # Ensuring test entity is only 1 token long.
                    t_i = (t_i[0], int(end_offsets[start_offsets.index(str(t_i[0]))]))
                    return (r_i, t_i)
                
                except Exception:
                    print(f'{doc_id} {r_i} {t_i} failed assertion')
    
    return None, None




def validate_relations(relations, docs, tokens_path):
    pubtator_data = []
    assert len(relations) == len(docs)
    for i, relations in enumerate(relations):
        doc_id = docs[i][0]
        doc = docs[i][1]

        doc_relations = []

        for relation in relations.split('\n'):
            if relation == '':
                continue
            try:
                rml_entity, tst_entity = relation.split(' | ')
            except ValueError:
                print(f'GPT made an oopsie - {relation}')
                continue
            rml_indexes = [(m.start(), m.end()) for m in re.finditer(re.escape(rml_entity), doc)]
            tst_indexes = [(m.start(), m.end()) for m in re.finditer(re.escape(tst_entity), doc)]
            rml_index, tst_index = check_rml_tst_same_sentence(rml_indexes, tst_indexes, doc_id, tokens_path)

            if rml_index:
                doc_relations.append((f'{rml_index[0]}-{rml_index[1]}', 
                                    f'{tst_index[0]}-{tst_index[1]}',
                                    rml_entity, tst_entity))

        pubtator_data.append((doc_id, doc_relations))
    return pubtator_data

def write_pubtator_data(lang, model_name, pubtator_data, docs):
    with open(f"results_{lang}/{model_name}.pubtator",
                'w') as f:
        for relations, doc in zip(pubtator_data, docs):
            # Confirming doc ids match
            assert relations[0] == doc[0]

            f.write(f'{doc[0]}|t|{doc[1]}\n')
            for relation in relations[1]:
                f.write(f"{doc[0]}\tREL\t{relation[0]}\t{relation[1]}\t{relation[2]}\t{relation[3]}\n")
            f.write('\n')