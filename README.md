# Automatic Clinical Relation Extraction

Task - Identifying test results and measurements within clinical documents in Italian, Spanish and Basque.

Dataset for Italian - https://e3c.fbk.eu/clinkart
Dataset for Spanish and Basque - https://e3c.fbk.eu/testlinkiberlef

### Preliminary Instructions
- Download the zip file of the datasets and keep them in the repo main folder.

## Fine-tuning Transformer models
Done in 2 stages
<figure>
<img src="re-schematic.png" width=75% height=75%>
<figcaption>Flowchart of the Relation Extraction training process</figcaption>
</figure>



3 models used for both stages - mBERT, XLM-Roberta and BERT

- `sh prepare_script.sh` - to prepare required data
- `python train.py` - entire train and validation
- `python train_full.py` - trains on the entire set(train+valid)
- `python predict.py` - predicts on the test set

## LLM Few shot learning

Few shot learning with gpt-4-turbo, gpt-4 and gpt-3.5-turbo

Files inside `LLMs\`