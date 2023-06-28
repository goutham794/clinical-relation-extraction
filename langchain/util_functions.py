import itertools

def get_examples_for_prompt(args):
    """
    Get example clincal statements to be used in the few-shot prompt.
    """
    with open(f"../{args.config.DATASET_PATH}") as file:
        data = file.readlines()

    data = [list(x[1]) for x in itertools.groupby(data, lambda x: x=='\n') if not x[0]] 
    
    examples_in_prompt = []

    for doc in data:
        doc_id = doc[0].split('|t|')[0]
        if doc_id not in args.prompt_config.few_shot_doc_ids:
            continue
        text_and_output = {}
        text_and_output['Text'] = doc[0].split('|t|')[1].strip()
        text_and_output['Output'] = ""

        for relation in doc[1:]:
            _,_,_, _, result_entity, test_entity = relation.split('\t')
            text_and_output['Output'] += f"{result_entity} | {test_entity.strip()}\n"

        examples_in_prompt.append(text_and_output)
    
    return examples_in_prompt