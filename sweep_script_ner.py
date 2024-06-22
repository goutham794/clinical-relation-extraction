from simpletransformers.ner import NERModel,NERArgs
import argparse
import logging
import torch

from config import Config

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])




def train():


    logging.info(f"Training NER model {args.model} model and train data.")

    model_config = args.config.model_args_ner 
    model_config['train_batch_size'] = args.batch_size
    model_config['output_dir']  = f"outputs_{args.lang}/{args.model}_ner/"
    model_config['best_model_dir']  = f"models_{args.lang}/{args.model}_ner/"
    model_config['learning_rate']  = args.learning_rate
    model_config['num_train_epochs']  = args.num_train_epochs
    model_config['scheduler']  = args.scheduler
    model_config['optimizer']  = args.optimizer
    model_config['weight_decay']  = args.weight_decay
    model_config['max_grad_norm']  = args.max_grad_norm
    model_config['warmup_ratio']  = args.warmup_ratio

    model_config['wandb_project']  = "ner_training_project"
    model_config['save_eval_checkpoints']  = False
    model_config['save_model_every_epoch']  = False


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
    parser.add_argument('--model', '-m', default="mbert")
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument("--batch_size", type=int)
    parser.add_argument("--num_train_epochs", '-e', type=int)
    parser.add_argument("--warmup_ratio", type=float)
    parser.add_argument("--learning_rate", type=float)
    parser.add_argument("--max_grad_norm", type=float)
    parser.add_argument("--weight_decay", type=float)
    parser.add_argument("--optimizer")
    parser.add_argument("--scheduler")

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]

    train()