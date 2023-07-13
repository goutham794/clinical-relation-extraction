import itertools
import argparse
import csv
from dataclasses import dataclass, field

from config import Config
import utils


@dataclass
class Token_Data:
    text: str
    start_offset: int
    end_offset: int
    tag: int = field(default=None)


class RE_Dataset:

    def __init__(self, args):
        self.tokens_file = f"data_{args.lang}/{args.split}{'_tokens' if args.split != 'train' else ''}.txt"
        self.offsets_file = f"data_{args.lang}/{args.split}_offsets.txt"
        self.config = args.config
        self.split = args.split
        self.lang = args.lang
        self.model = args.model

        self.tokens_set = self.read_tokens()
        if args.split == 'train':
            self.relations = self.read_relations()
            self.re_dataset = self.create_train_dataset()
        else:
            self.relations = self.create_relations_from_preds()
            self.re_dataset = self.create_dataset()

        self.write_dataset_to_file()
    
    def read_tokens(self):

        with open(self.tokens_file) as f1 , open(self.offsets_file) as f2:
            all_tokens = []
            sentence_tokens = []
            for l1, l2 in zip(f1, f2):
                if l1 == "\n":
                    assert l2 == "\n"
                    all_tokens.append((doc_id, sentence_tokens))
                    sentence_tokens = []
                    continue
                doc_id = l2.split()[0]
                start_offset = int(l2.split()[2])
                end_offset = int(l2.split()[3])
                if self.split == 'train':
                    token, tag = l1.strip().split()
                    sentence_tokens.append(Token_Data(text=token, tag=tag, 
                            start_offset=start_offset, end_offset=end_offset))
                else:
                    token = l1.strip()
                    sentence_tokens.append(Token_Data(text=token,
                            start_offset=start_offset, end_offset=end_offset))

        return [x for x in all_tokens if any([t.tag!='O' for t in x[1]])]
    
    def read_relations(self, train=True):

        with open(self.config.DATASET_PATH) as file:
            training_data = file.readlines()

        training_data = [list(x[1]) for x in itertools.groupby(training_data, lambda x: x=='\n') if not x[0]] 
        relations = {}

        for data in training_data:
            doc_id = data[0].split('|t|')[0]
            if train == (doc_id in self.config.VALID_DOC_IDS):
                continue
            
            relations[doc_id] = []
            for relation in data[1:]:
                _,_,result_offset, test_offset, _, _ = relation.split('\t')
                relations[doc_id].append((tuple(result_offset.split('-')), 
                                               tuple(test_offset.split('-'))))
        return relations
        
    @staticmethod
    def recreate_line(relation, tokens):
        relation = tuple((int(r[0]), int(r[1])) for r in relation)
        initial_start_offset = tokens[0].start_offset
        labels_and_offsets = [tuple(['[RML]',r - initial_start_offset]) for r in relation[0]] + [tuple(['[TST]',r - initial_start_offset]) for r in relation[1]]
        labels_and_offsets = sorted(labels_and_offsets, key=lambda x: x[1], reverse=True)
        line = ""
        for token in tokens:
            line += " "*(token.start_offset - initial_start_offset - len(line))                    
            assert token.start_offset == len(line) + initial_start_offset
            line += token.text
        line = list(line)
        for label, offset in labels_and_offsets:
            assert 0 <= offset <= len(line)
            line[offset:offset] = label
        return ''.join(line)


    def create_relations_from_preds(self):
        relations = []
        entity_offsets = utils.get_predicted_entity_offsets(f'results_{self.lang}/preds_{self.model}_{args.split}_ner.txt', 
                                           self.offsets_file)
        for sent_entity_offsets in entity_offsets:
            relations.append([(x,y) for x in sent_entity_offsets[0] for y in sent_entity_offsets[1]])

        return relations

    def create_dataset(self):
        re_dataset = []
        for sent_relations, sentence in zip(self.relations, self.tokens_set):
            doc_id, tokens = sentence
            for relation in sent_relations:
                line = RE_Dataset.recreate_line(relation, tokens)
                re_dataset.append((doc_id, line, relation[0][0], relation[0][1],
                                   relation[1][0], relation[1][1])) 
        return re_dataset
    

    def create_train_dataset(self):
        re_dataset = []
        for sentence in self.tokens_set:
            doc_id, tokens = sentence
            rml_start_offsets = [t.start_offset for t in tokens if t.tag=='B-RML']
            positive_relations = [r for r in self.relations[doc_id] if int(r[0][0]) in rml_start_offsets]
            neg_relations = set([(x,y) for y in [i for _,i in positive_relations] for x,_ in positive_relations if (x,y) not in positive_relations])
            for relation in positive_relations:
                line = RE_Dataset.recreate_line(relation, tokens)
                re_dataset.append((doc_id, line, 1, relation[0][0], relation[0][1],
                                   relation[1][0], relation[1][1])) 
            for relation in neg_relations:
                line = RE_Dataset.recreate_line(relation, tokens)
                re_dataset.append((doc_id, line, 0, relation[0][0], relation[0][1],
                                   relation[1][0], relation[1][1])) 
                
        return re_dataset
    

    @staticmethod
    def get_stats(re_dataset):
        print(len(re_dataset))
        print(len([i for i in re_dataset if i[1]==1])/len(re_dataset))
        print(len([i for i in re_dataset if i[1]==0])/len(re_dataset))

    def write_dataset_to_file(self):
        with open(f"data_{args.lang}/{args.split}_{args.model}_{'full_' if args.use_full_train else ''}re_dataset.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in self.re_dataset:
                writer.writerow(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--split', '-s', default='test')
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument('--use-full-train', default=False, 
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    if args.use_full_train: assert args.split == 'train'
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs

    re_data = RE_Dataset(args)