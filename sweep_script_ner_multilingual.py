from simpletransformers.ner import NERModel,NERArgs
import argparse
import logging
import torch
import wandb

from config import Config

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])




def train():

    logging.info(f"Training NER model {args.model} model on multilingual train data.")

    model_config = args.config.model_args_ner 
    model_config['train_batch_size'] = args.batch_size
    model_config['output_dir']  = f"outputs_multilingual/{args.model}_ner/"
    model_config['best_model_dir']  = f"models_multilingual/{args.model}_ner/"
    model_config['learning_rate']  = args.learning_rate
    model_config['num_train_epochs']  = args.num_train_epochs
    model_config['scheduler']  = args.scheduler
    model_config['optimizer']  = args.optimizer
    model_config['weight_decay']  = args.weight_decay
    model_config['max_grad_norm']  = args.max_grad_norm
    model_config['warmup_ratio']  = args.warmup_ratio

    model_config['wandb_project']  = "ner_training_project"


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
    parser.add_argument('--model', '-m', default="biobert")
    parser.add_argument("--batch_size", type=int)
    parser.add_argument("--num_train_epochs", '-e', type=int)
    parser.add_argument("--warmup_ratio", type=float)
    parser.add_argument("--learning_rate", type=float)
    parser.add_argument("--max_grad_norm", type=float)
    parser.add_argument("--weight_decay", type=float)
    parser.add_argument("--optimizer")
    parser.add_argument("--scheduler")

    args = parser.parse_args()
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config('it')
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]

    train()