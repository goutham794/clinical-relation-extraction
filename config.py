class Config:
    def __init__(self, lang) -> None:
        self.lang = lang

        if lang == 'it':
            self.set_Italian_config()    
        elif lang == 'es':
            self.set_Spanish_config()
        elif lang == "eu":
            self.set_Basque_config()
        else:
            self.set_Multilingual_config()
        
        self.WANDB_API_KEY = "471331f912e2b2e7a3d6007c7cce37cccd3dca4c"

        self.NER_CLASSES = ["O", "B-TST", "B-RML", "I-TST", "I-RML"]
        self.TEST_ENTITY_MARKER = "[TST]"
        self.RESULT_ENTITY_MARKER = "[RML]"
        self.pretrained_model_details = {'mbert': ("bert", "bert-base-multilingual-cased"),
            'xlmroberta': ("xlmroberta", "xlm-roberta-base"), 
            'biobert': ("bert", "dmis-lab/biobert-v1.1"), 
            'bert': ("bert", "bert-base-uncased")}
        self.model_args_ner = {
            "manual_seed" : 42,
            "evaluate_during_training" : True,
            "overwrite_output_dir" :True,
            "max_seq_length" : 512,
            'save_eval_checkpoints' : False,
            'save_model_every_epoch' : False
            }
        self.model_args_rc = {
            "manual_seed" : 42,
            "evaluate_during_training" : True,
            "overwrite_output_dir" :True,
            "max_seq_length" : 512,
            'save_eval_checkpoints' : False,
            'save_model_every_epoch' : False,
            'use_multiprocessing_for_evaluation' : False,
            'use_multiprocessing' : False
            }
    

    

    def set_Italian_config(self):
        self.DATASET_PATH = "Clinkart_training_data/training.txt"
        self.TOKEN_DATA_PATH = "Clinkart_training_data/training_tokenized"
        self.TEST_DATASET = "TEST_IT/gold_test_set.pubtator"
        self.TEST_TOKEN_DATA = "TEST_IT/test_tokenized"
        self.VALID_DOC_IDS = ['101165', '100803', '101137', '101146', '101139', '100990', '100759', '101167', '100742', '101073', '100460', '101191']
        self.RELATIONS_TO_EXCLUDE = []

    def set_Spanish_config(self):
        self.DATASET_PATH = "TESTLINK_ES_training_data_v1.1/TESTLINK_training_data/training.txt"
        self.TEST_DATASET = "TEST_ES/gold_test_set.pubtator"
        self.TOKEN_DATA_PATH = "TESTLINK_ES_training_data_v1.1/training_tokenized"
        self.TEST_TOKEN_DATA= "TEST_ES/test_tokenized"
        self.VALID_DOC_IDS = ['100962', '100278', '100775', '100705', '100947', '100280', '100840', '100050', '100284', '100259', '100791', '100789']
        self.RELATIONS_TO_EXCLUDE = []

    def set_Basque_config(self):
        self.DATASET_PATH = "TESTLINK_EU_training_data/training.txt"
        self.TEST_DATASET = "TEST_EU/gold_test_set.pubtator"
        self.TOKEN_DATA_PATH = "TESTLINK_EU_training_data/training_tokenized"
        self.TEST_TOKEN_DATA = "TEST_EU/test_tokenized"
        self.VALID_DOC_IDS = ['100031', '100171', '100078', '100043', '100017', '100103', '100021', '100189', '100024', '100110', '100146', '100126', '100008']
        self.RELATIONS_TO_EXCLUDE = [(('1975', '1982'), ('1959', '1972')), (('1093', '1102'), ('1076', '1077')), (('1093', '1102'), ('1067', '1075'))]
    
    def set_Multilingual_config(self):
        self.DATASET_PATH = "Multilingual_data/training.txt"
        self.TOKEN_DATA_PATH = "Clinkart_training_data/training_tokenized"
        self.VALID_DOC_IDS = ['101165', '100803', '101137', '101146', '101139', '100990', '100759', '101167', '100742', '101073', '100460', '101191', 
                              '100962', '100278', '100775', '100705', '100947', '100280', '100840', '100050', '100284', '100259', '100791', '100789', 
                            '100031', '100171', '100078', '100043', '100017', '100103', '100021', '100189', '100024', '100110', '100146', '100126', '100008']
        self.RELATIONS_TO_EXCLUDE = [(('1975', '1982'), ('1959', '1972')), (('1093', '1102'), ('1076', '1077')), (('1093', '1102'), ('1067', '1075'))]



    

