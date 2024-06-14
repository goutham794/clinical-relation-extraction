from simpletransformers.ner import NERModel,NERArgs
import argparse
import wandb
import logging
import torch

from config import Config


logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])




def Train_NER():


    run = wandb.init(job_type="train")
    config = run.config

    logging.info(f"Training NER model {args.model} model and {'combined' if args.use_full_train else 'split'} train data.")

    model_config = args.config.model_args_ner 
    model_config['train_batch_size'] = args.batch_size
    model_config['output_dir']  = f"outputs_{args.lang}/{args.model}_ner/"
    model_config['best_model_dir']  = f"models_{args.lang}/{args.model}_ner{'_combined' if args.use_full_train else ''}/"
    model_config['learning_rate']  = config.learning_rate
    model_config['num_train_epochs']  = config.num_train_epochs
    model_config['wandb_project']  = "ner_training_project"

    model_args = NERArgs()
    model_args.update_from_dict(model_config)

    custom_labels = args.config.NER_CLASSES

    model = NERModel(
        args.model_type, args.model_name, args=model_args, labels=custom_labels,
    )

    x = model.train_model(f"data_{args.lang}/train{'_full' if args.use_full_train else ''}.txt", 
                      eval_data=f"data_{args.lang}/valid.txt"
                      )
    torch.cuda.empty_cache()
    run.finish()

def main():
    sweep_config = {
            'method': 'bayes',  # grid, random, bayesian optimization
            'metric': {
                'name': 'f1_score',
                'goal': 'maximize'
            },
            'parameters': {
                'learning_rate': {
                    'values': [5e-5, 3e-5, 2e-5]
                },
                'batch_size': {
                    'values': [16, 32, 64]
                },
                'num_train_epochs': {
                'values': [3, 4, 5]
                }
            }
        }
    sweep_id = wandb.sweep(sweep_config, project="ner_training_project")
    wandb.agent(sweep_id, Train_NER, count=10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--use-full-train', default=False, 
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument("--batch-size", type=int, default = 16)
    parser.add_argument("--epochs", '-e', type=int, default = 1)
    parser.add_argument("--lr", default=0.0001, type=float)

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]

    main()