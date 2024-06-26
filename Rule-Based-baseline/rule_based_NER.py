import re
from seqeval.metrics import classification_report

import config

class Rule_Based_NER:
    def __init__(self, valid_tokens_file, rml_regexes) -> None:
        self.valid_tokens_file = valid_tokens_file
        self.rml_regexes = rml_regexes

    def fetch_train_entities(self):
        test_entities = []
        rml_entities = []
        with open("train.txt", 'r') as f:
            intermediate_test_entity = []
            intermediate_rml_entity = []
            for row in f.readlines():
                if row == '\n':
                    continue
                token, tag = row.strip().split()
                if intermediate_test_entity != []:
                    if tag == 'I-TST':
                        intermediate_test_entity.append(token)
                    else:
                        test_entities.append(tuple(intermediate_test_entity))
                        intermediate_test_entity = []
                        if tag == 'O':
                            continue

                if intermediate_rml_entity != []:
                    if tag == 'I-RML':
                        intermediate_rml_entity.append(token)
                    else:
                        rml_entities.append(tuple(intermediate_rml_entity))
                        intermediate_rml_entity = []
                        if tag == 'O':
                            continue
                
                if tag == 'B-TST':
                    intermediate_test_entity.append(token)
                    continue

                if tag == 'B-RML':
                    intermediate_rml_entity.append(token)
                    continue
        
        self.train_tst_entities = set(test_entities) 
        [self.train_tst_entities.remove(i) for i in config.TST_ENTITIES_TO_REMOVE]
        self.train_rml_entities = set(rml_entities) 



    def get_validation_set_tokens(self):
        validation_set_tokens= []
        validation_set_tags = []
        validation_sentence_tokens = []
        validation_sentence_tags = []
        with open("valid.txt", 'r') as f:
            for row in f.readlines():
                if row == '\n':
                    validation_set_tokens.append(validation_sentence_tokens)
                    validation_set_tags.append(validation_sentence_tags)
                    validation_sentence_tokens = []
                    validation_sentence_tags = []
                    continue

                token, tag = row.strip().split()
                validation_sentence_tokens.append(token)
                validation_sentence_tags.append(tag)

        self.validation_set_tokens = validation_set_tokens
        self.validation_set_tags = validation_set_tags
        self.validation_set_labels = [['O']*len(x) for x in self.validation_set_tokens]
        token_count = 0
        self.cumulative_token_count = []
        for sentence_tokens in self.validation_set_tokens:
            token_count += len(sentence_tokens)+1
            self.cumulative_token_count.append(token_count)



    def set_validation_tst_entity_predictions(self):
        for entity in self.train_tst_entities:
            for sent_num, validation_sentence_tokens in enumerate(self.validation_set_tokens):
                token_tuples = [tuple(validation_sentence_tokens[i:i+len(entity)]) for i in range(len(validation_sentence_tokens)-(len(entity)-1))]
                match_indices = [i for i in range(len(token_tuples)) if token_tuples[i] == entity]
                for match_index in match_indices:
                    try:
                        assert self.validation_set_labels[sent_num][match_index:match_index+len(entity)] == ['O'] * len(entity) 
                    except AssertionError:
                        existing_entity_len = 1
                        for label in self.validation_set_labels[sent_num][match_index+1:]:
                            if (label != "I-TST"):
                                break
                            existing_entity_len += 1
                        if existing_entity_len > len(entity):
                            continue
                    self.validation_set_labels[sent_num][match_index:match_index+len(entity)] = ["B-TST"] + ["I-TST"] * (len(entity) - 1)


    @staticmethod
    def match_entity_in_sentence(sentence_tokens, entity):
        match_index = None
        for i in range(len(sentence_tokens)-(len(entity)-1)):
            if sentence_tokens[i:i+len(entity)] == entity:
                match_index = i
                break
        return match_index
    

    def get_line_number(self, char_num):
        with open(self.valid_tokens_file, 'r') as f:
            line_num = 0
            for line in f:
                line_num += 1
                if char_num <= len(line):
                    return line_num
                char_num -= len(line)
            return None

    def set_rml_validation_labels(self, start, end):
        for index, token_count in enumerate(reversed(self.cumulative_token_count)):
            if token_count <= start:
                sentence_num = index
                break
        sentence_num = len(self.cumulative_token_count) - sentence_num
        assert self.validation_set_labels[sentence_num][(start-self.cumulative_token_count[sentence_num]+1):(end-self.cumulative_token_count[sentence_num]+1)] == ['O'] * (end - start)
        self.validation_set_labels[sentence_num][(start-self.cumulative_token_count[sentence_num]+1):(end-self.cumulative_token_count[sentence_num]+1)] = ["B-RML"] + ["I-RML"] * (end - start - 1)

    



    def set_validation_rml_entity_predictions(self):
        with open("valid_tokens.txt") as f:
            valid_tokens = f.read()
            for pattern in self.rml_regexes:
                for match in re.finditer(pattern, valid_tokens, flags=re.IGNORECASE):
                    start_line = self.get_line_number(match.start())
                    end_line = self.get_line_number(match.end())
                    self.set_rml_validation_labels(start_line, end_line)
    
    def write_predictions_to_file(self):
        with open("valid_predictions.txt", 'w') as f:
            for sent_num,sentence in enumerate(self.validation_set_tokens):
                for token_num, token in enumerate(sentence):
                    f.write(f"{token} {self.validation_set_tags[sent_num][token_num]} {self.validation_set_labels[sent_num][token_num]}\n") 

    def calculate_metrics(self):
        print(classification_report(self.validation_set_tags, self.validation_set_labels))

            

rule_based = Rule_Based_NER("valid_tokens.txt", config.RML_REGEX_PATTERNS)
rule_based.fetch_train_entities()
rule_based.get_validation_set_tokens()
rule_based.set_validation_tst_entity_predictions()
rule_based.set_validation_rml_entity_predictions()
rule_based.write_predictions_to_file()
rule_based.calculate_metrics()