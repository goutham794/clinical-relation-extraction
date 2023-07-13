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
        args.model_type, 
        f"models_{args.lang}/{args.model}_ner{'_combined' if args.split == 'test' else ''}",
          args=model_args, labels=custom_labels
    )

    tokens = utils.create_tokens_list_from_file(f"data_{args.lang}/{args.split}_tokens.txt")
    predictions, _ = model.predict(tokens, split_on_space=False)
    predictions = [[list(d.values())[0] for d in i] for i in predictions]
    utils.save_predictions_to_file(predictions, args.lang, f'preds_{args.model}_{args.split}_ner.txt')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--split', '-s', default='test')
    parser.add_argument('--lang', '-l', default='it')

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]
    Infer_NER(args)