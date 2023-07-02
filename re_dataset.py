import itertools
import argparse
import csv

from config import Config

class RE_Dataset:

    def __init__(self, args):
        self.tokens_file = args.tokens_file
        self.offsets_file = args.offsets_file
        self.config = args.config

        self.tokens_set = self.read_tokens()
        self.relations = self.read_relations()
        self.re_dataset = self.create_dataset()
    
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
                token, tag = l1.strip().split()
                sentence_tokens.append((token, tag, start_offset, end_offset))

        return [x for x in all_tokens if any([t[1]!='O' for t in x[1]])]
    
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
        initial_start_offset = tokens[0][2]
        labels_and_offsets = [tuple(['[TST]',r - initial_start_offset]) for r in relation[0]] + [tuple(['[RML]',r - initial_start_offset]) for r in relation[1]]
        labels_and_offsets = sorted(labels_and_offsets, key=lambda x: x[1], reverse=True)
        line = ""
        for token in tokens:
            line += " "*(token[2] - initial_start_offset - len(line))                    
            assert token[2] == len(line) + initial_start_offset
            line += token[0]
        line = list(line)
        for label, offset in labels_and_offsets:
            assert 0 <= offset <= len(line)
            line[offset:offset] = label
        return ''.join(line)



    def create_dataset(self, split='train'):
        token_set = self.train_set_tokens if split == 'train' else self.valid_set_tokens
        relations_set = self.train_relations if split == 'train' else self.valid_relations
        re_dataset = []
        for sentence in token_set:
            doc_id, tokens = sentence
            rml_start_offsets = [t[2] for t in tokens if t[1]=='B-RML']
            positive_relations = [r for r in relations_set[doc_id] if int(r[0][0]) in rml_start_offsets]
            neg_relations = set([(x,y) for y in [i for _,i in positive_relations] for x,_ in positive_relations if (x,y) not in positive_relations])
            for relation in positive_relations:
                line = RE_Dataset.recreate_line(relation, tokens)
                re_dataset.append((line,1)) 
            for relation in neg_relations:
                line = RE_Dataset.recreate_line(relation, tokens)
                re_dataset.append((line,0)) 
                
        return re_dataset
    

    @staticmethod
    def get_stats(re_dataset):
        print(len(re_dataset))
        print(len([i for i in re_dataset if i[1]==1])/len(re_dataset))
        print(len([i for i in re_dataset if i[1]==0])/len(re_dataset))

    def write_dataset_to_file(self):
        with open("data/train_re_dataset.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in self.train_re_dataset:
                writer.writerow(line)

        with open("data/valid_re_dataset.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in self.valid_re_dataset:
                writer.writerow(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--split', '-s', default='valid')
    parser.add_argument('--lang', '-l', default='it')

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs


    args.tokens_file = f"data_{args.lang}/{args.split}_tokens.txt"
    args.tokens_file = f"data_{args.lang}/{args.split}_offsets.txt"
    re_data = RE_Dataset(args)