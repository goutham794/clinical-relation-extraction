from simpletransformers.ner import NERModel,NERArgs
import argparse
import wandb
import logging
import torch

from config import Config
from sweep_configs import SWEEP_CONFIGS


logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])




def Train_NER():


    run = wandb.init(job_type="train")
    config = run.config

    logging.info(f"Training NER model {args.model} model and {'combined' if args.use_full_train else 'split'} train data.")

    model_config = args.config.model_args_ner 
    model_config['train_batch_size'] = config.batch_size
    model_config['output_dir']  = f"outputs_multilingual/{args.model}_ner/"
    model_config['best_model_dir']  = f"models_mulilingual/{args.model}_ner{'_combined' if args.use_full_train else ''}/"
    model_config['learning_rate']  = config.learning_rate
    model_config['num_train_epochs']  = config.num_train_epochs
    model_config['scheduler']  = config.scheduler
    model_config['optimizer']  = config.optimizer
    model_config['wandb_project']  = "ner_training_project"

    model_args = NERArgs()
    model_args.update_from_dict(model_config)

    custom_labels = args.config.NER_CLASSES

    model = NERModel(
        args.model_type, args.model_name, args=model_args, labels=custom_labels,
    )

    x = model.train_model(f"data_multilingual/train{'_full' if args.use_full_train else ''}.txt", 
                      eval_data=f"data_multilingual/valid.txt"
                      )
    torch.cuda.empty_cache()
    run.finish()

def main():
    sweep_config = SWEEP_CONFIGS['NER'][args.model]
    sweep_id = wandb.sweep(sweep_config, project=f"{args.model}_multilingual_ner_task")
    wandb.agent(sweep_id, Train_NER, count=15)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--use-full-train', default=False, 
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config("it")
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]

    main()