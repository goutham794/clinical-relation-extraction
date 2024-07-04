from simpletransformers.ner import NERModel,NERArgs
import argparse
import logging
from utils import fetch_optimal_hyperparams

from config import Config


logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def Train_NER(args):

    logging.info(f"Training NER model {args.model} model and train data.")

    optimal_hyperparam_dict = fetch_optimal_hyperparams("ner", args.model, "multilingual")

    model_config = args.config.model_args_ner 
    model_config['output_dir']  = f"outputs_multilingual/{args.model}_ner/"
    model_config['best_model_dir']  = f"models_multilingual/{args.model}_ner/"
    model_config['wandb_project'] = f"ner_{args.model}_multilingual_final" 

    model_config.update(optimal_hyperparam_dict)
    # rename wrongly named key.
    model_config['train_batch_size'] = model_config.pop("batch_size")

    model_args = NERArgs()
    model_args.update_from_dict(model_config)

    custom_labels = args.config.NER_CLASSES

    model = NERModel(
        args.model_type, args.model_name, args=model_args, labels=custom_labels,
    )

    x = model.train_model(f"data_multilingual/train.txt", 
                      eval_data=f"data_multilingual/valid.txt"
                      )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    args = parser.parse_args()
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config("multilingual")
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]

    Train_NER(args)