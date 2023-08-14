# Automatic Clinical Relation Extraction

Task - Identifying test results and measurements within clinical documents in Italian, Spanish and Basque.

Dataset for Italian - https://e3c.fbk.eu/clinkart
Dataset for Spanish and Basque - https://e3c.fbk.eu/testlinkiberlef

### Preliminary Instructions
- Download the zip file of the datasets and keep them in the repo main folder.

## Fine-tuning Transformer models

![Flowchart of the Relation Extraction training process](re-schematic.png)

3 models used for both stages - mBERT, XLM-Roberta and BERT

-`sh prepare_script.sh` - to prepare required data
-`python train.py` - entire train and validation
-`python predict.py` - trains on the entire set(train+valid) and predicts on the test set

## LLM Few shot learning

Used langchain with GPT 3.5 API
GPT 4 to be tested

Files inside `langchain\`
`python chain_train.py` 

## LLM Fine-tuning with QLORA 

WIP. 
Working on Llama2 7B and Falcon 7B
