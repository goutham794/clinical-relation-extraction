from simpletransformers.ner import NERModel,NERArgs
import argparse
import os
import logging

from config import Config
import utils

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def Infer_NER(args):

    logging.info(f"Inference with NER model {args.model} model on {args.split} split")

    model_config = args.config.model_args_ner 

    model_args = NERArgs()
    model_args.update_from_dict(model_config)

    custom_labels = args.config.NER_CLASSES

    model = NERModel(
        args.model_type, "models_it/mbert_ner", args=model_args, labels=custom_labels
    )

    tokens = utils.create_tokens_list_from_file(f"data_{args.lang}/valid_tokens.txt")
    predictions, _ = model.predict(tokens, split_on_space=False)
    utils.save_predictions_to_file(predictions, args.lang, f'preds_{args.model}_ner')



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
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]
    Infer_NER(args)