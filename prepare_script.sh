#!/bin/bash
# set -e

mkdir data_it/
mkdir data_es/
mkdir data_eu/

mkdir TEST_IT/
mkdir TEST_ES/
mkdir TEST_EU/

mkdir results_it/
mkdir results_es/
mkdir results_eu/

unzip Clinkart_training_data.zip
unzip Clinkart_test_data.zip -d TEST_IT/
unzip TESTLINK_ES_training_data_v1.1.zip
unzip TESTLINK_ES_test_data_v1.0.zip -d TEST_ES/
unzip TESTLINK_EU_training_data.zip
unzip TESTLINK_EU_test_data_v1.0.zip -d TEST_EU/

unzip BC5CDR_Evaluation-0.0.3.zip

unzip TESTLINK_ES_training_data_v1.1/TESTLINK_ES_training_data.zip -d TESTLINK_ES_training_data_v1.1/
unzip TESTLINK_ES_training_data_v1.1/training_tokenized.zip -d TESTLINK_ES_training_data_v1.1/
unzip TESTLINK_EU_training_data/training_tokenized.zip -d TESTLINK_EU_training_data/

unzip TEST_IT/test_tokenized.zip -d TEST_IT/
unzip TEST_ES/test_tokenized.zip -d TEST_ES/
unzip TEST_EU/test_tokenized.zip -d TEST_EU/

python prepare_conll_txt.py -l 'it'
python prepare_conll_test_data.py -l 'it'

python prepare_conll_txt.py -l 'es'
python prepare_conll_test_data.py -l 'es'

python prepare_conll_txt.py -l 'eu'
python prepare_conll_test_data.py -l 'eu'

python create_valid_pubtators.py -l 'it'
python create_valid_pubtators.py -l 'es'
python create_valid_pubtators.py -l 'eu'