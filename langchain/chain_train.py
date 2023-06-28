import argparse
import itertools
import re
from tqdm import tqdm
import logging
import sys
sys.path.append("../.")

from langchain.callbacks import get_openai_callback

from config import Config
from llm_chain import get_llm_chain
from util_functions import get_examples_for_prompt
from prompt_config import Prompt_Config
from prompt_creator import get_prompt

logger = logging.getLogger('prompt_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('prompts.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

class GPT_Relation_Extractor:
    def __init__(self, args) -> None:
        self.lang = args.lang
        self.args = args
        self.pubtator_data = []

        self.read_clinical_docs()
        self.extract_relations()
        self.validate_relations()
        self.write_pubtator_data()
    
    def read_clinical_docs(self):
        
        self.docs = []

        with open(f"../{self.args.config.DATASET_PATH}") as file:
            data = file.readlines()

        data = [list(x[1]) for x in itertools.groupby(data, lambda x: x=='\n') if not x[0]] 

        for doc in data:
            statement_id = doc[0].split('|t|')[0]
            self.docs.append((statement_id,  doc[0].split('|t|')[1].strip()))
    
    def extract_relations(self):
        self.relations = []
        cost = 0
        for doc in tqdm(self.docs[:args.num_of_docs_to_infer]):
        # for doc in tqdm(self.docs):
            self.args.new_clinical_stmt = doc[1]
            self.args.examples = get_examples_for_prompt(args)
            prompt = get_prompt(self.args)
            logger.info(prompt)
            chain = get_llm_chain(prompt, args)
            with get_openai_callback() as cb:
                self.relations.append(chain.run(doc))
                cost += cb.total_cost
        logger.info(f"Cost = {cost}")

    
    @staticmethod
    def check_rml_tst_same_sentence(rml_indexes, tst_indexes, doc_id):
        """
        Returns indexes of eml and test entity that belong to same sentence or `None` otherwise.
        """
        with open(f"../{args.config.TOKEN_DATA_PATH}/{doc_id}.tsv") as file:
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

    
    def validate_relations(self):
        for i, relations in enumerate(self.relations):
            doc_id = self.docs[i][0]
            doc = self.docs[i][1]

            doc_relations = []

            for relation in relations.split('\n'):
                if relation == '':
                    continue
                try:
                    rml_entity, tst_entity = relation.split(' | ')
                except ValueError:
                    print(f'GPT made an oopsie - {relation}')
                    continue
                rml_indexes = [(m.start(), m.end()) for m in re.finditer(rml_entity, doc)]
                tst_indexes = [(m.start(), m.end()) for m in re.finditer(tst_entity, doc)]
                rml_index, tst_index = GPT_Relation_Extractor.check_rml_tst_same_sentence(rml_indexes, tst_indexes, doc_id)

                if rml_index:
                    doc_relations.append((f'{rml_index[0]}-{rml_index[1]}', 
                                      f'{tst_index[0]}-{tst_index[1]}',
                                      rml_entity, tst_entity))

            self.pubtator_data.append((doc_id, doc_relations))
    
    def write_pubtator_data(self):
        # with open(f"results_{self.lang}/gpt_{args.num_of_docs_to_infer}.pubtator", 'w') as f:
        with open(f"results_{self.lang}/gpt.pubtator", 'w') as f:
            for relations, doc in zip(self.pubtator_data, self.docs):
                # Confirming doc ids match
                assert relations[0] == doc[0]

                f.write(f'{doc[0]}|t|{doc[1]}\n')
                for relation in relations[1]:
                    f.write(f"{doc[0]}\tREL\t{relation[0]}\t{relation[1]}\t{relation[2]}\t{relation[3]}\n")
                f.write('\n')




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument('--llm-service', '-s', default='openai')
    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.llm_service in ['azure', 'openai'], "LLM service must be one of azure or openai"

    configs = Config(args.lang)
    args.config = configs
    
    prompt_config = Prompt_Config(args.lang)

    args.prompt_config = prompt_config

    args.num_of_docs_to_infer = 3

    gpt_1 = GPT_Relation_Extractor(args)