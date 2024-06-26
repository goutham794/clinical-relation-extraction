from simpletransformers.classification import ClassificationModel, ClassificationArgs
import argparse
import pandas as pd
import logging
import os
import numpy as np
import wandb

from config import Config
import utils

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def train():

    wandb.init()
    class CustomClassificationModel(ClassificationModel):
        def eval_model(self, eval_df, multi_label=False, output_dir=None, verbose=True, silent=False, wandb_log=True, **kwargs):
            predictions, _ = self.predict(list(eval_df.text))
            utils.save_predicted_pubtator(eval_df[np.array(predictions).astype(bool)],args.lang, 
                            f"{args.model}_predicted_valid_set.pubtator", 
                            args.config.DATASET_PATH, args.config.TEST_ENTITY_MARKER, 
                            args.config.RESULT_ENTITY_MARKER)
            
            
            metrics = utils.get_pubtator_scores(args.lang, args.model, 'valid')
            metrics = {k: float(v) for k, v in metrics.items()}
            logging.info(metrics)
            wandb.log({'re_precision' : metrics['Precision']} )
            wandb.log({'re_recall' : metrics['Recall']} )
            wandb.log({'re_f1' : metrics['F-score']} )
            return metrics, _, _

    logging.info(f"Training RC model {args.model} model for {args.lang} train data.")

    df_train = pd.read_csv(f"data_{args.lang}/train_{args.model}_re_dataset.csv",
                           )
    df_train.columns = ["doc_id", "text", "labels", "rml_s", "rml_e", "tst_s", "tst_e"]

    df_eval = pd.read_csv(f"data_{args.lang}/valid_{args.model}_re_dataset.csv",
                           )
    df_eval.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]
    
    model_config = args.config.model_args_rc 
    model_config['train_batch_size'] = args.batch_size
    model_config['output_dir']  = f"outputs_{args.lang}/{args.model}_re/"
    model_config['best_model_dir']  = f"models_{args.lang}/{args.model}_re/"
    model_config['learning_rate']  = args.learning_rate
    model_config['num_train_epochs']  = args.num_train_epochs
    model_config['scheduler']  = args.scheduler
    model_config['optimizer']  = args.optimizer
    model_config['weight_decay']  = args.weight_decay
    model_config['max_grad_norm']  = args.max_grad_norm
    model_config['warmup_ratio']  = args.warmup_ratio

    model_config['wandb_project']  = "rc_training_project"
    model_config['labels_list'] = [0, 1]
    model_config['use_multiprocessing'] = False
    model_config['use_multiprocessing_for_evaluation'] = False
    model_config['early_stopping_metric'] = "F-score"

    model_args = ClassificationArgs()
    model_args.update_from_dict(model_config)

    model = CustomClassificationModel(
        args.model_type, args.model_name, args=model_args
    )

    model.train_model(df_train[["text", "labels"]], 
                      eval_df=df_eval)

        

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