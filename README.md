# Automatic Clinical Relation Extraction

## Fine-tuning Transformer models

![Flowchart of the Relation Extraction training process](re-schematic.png)

3 models used for both stages

- mBERT
- XLM-Roberta
- BERT

`prepare_script.sh` - to prepare required data
`train.py` - entire train and validation
`predict.py` - trains on the entire set(train+valid) and predicts on the test set

## LLM Few shot learning

Used langchain with GPT 3.5 API
GPT 4 to be tested

Files inside `langchain\`

## LLM Fine-tuning with QLORA 

WIP. 
Working on Llama2 7B and Falcon 7B
