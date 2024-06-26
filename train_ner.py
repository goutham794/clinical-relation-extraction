from simpletransformers.ner import NERModel,NERArgs
import argparse
import logging
from utils import fetch_optimal_hyperparams

from config import Config


logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def Train_NER(args):

    logging.info(f"Training NER model {args.model} model and {'combined' if args.use_full_train else 'split'} train data.")

    optimal_hyperparam_dict = fetch_optimal_hyperparams("ner", args.model, args.lang)

    model_config = args.config.model_args_ner 
    model_config['output_dir']  = f"outputs_{args.lang}/{args.model}_ner/"
    model_config['best_model_dir']  = f"models_{args.lang}/{args.model}_ner{'_combined' if args.use_full_train else ''}/"
    model_config['evaluate_during_training'] = True
    model_config['wandb_project'] = f"ner_{args.model}_{args.lang}_final" 

    model_config.update(optimal_hyperparam_dict)
    # rename wrongly named key.
    model_config['train_batch_size'] = model_config.pop("batch_size")

    model_args = NERArgs()
    model_args.update_from_dict(model_config)

    custom_labels = args.config.NER_CLASSES

    model = NERModel(
        args.model_type, args.model_name, args=model_args, labels=custom_labels,
    )

    x = model.train_model(f"data_{args.lang}/train{'_full' if args.use_full_train else ''}.txt", 
                      eval_data=f"data_{args.lang}/valid.txt"
                      )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--use-full-train', default=False, 
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--lang', '-l', default='it')

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]

    Train_NER(args)