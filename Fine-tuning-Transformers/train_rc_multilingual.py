from simpletransformers.classification import ClassificationModel, ClassificationArgs
import argparse
import pandas as pd
import logging
import os
import numpy as np
import wandb
from utils import fetch_optimal_hyperparams

from config import Config
import utils

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def Train_RC(args):

    class CustomClassificationModel(ClassificationModel):
        def eval_model(self, eval_df, multi_label=False, output_dir=None, verbose=True, silent=False, wandb_log=True, **kwargs):
            predictions, _ = self.predict(list(eval_df.text))
            utils.save_predicted_pubtator(eval_df[np.array(predictions).astype(bool)],"multilingual", 
                            f"{args.model}_predicted_valid_set.pubtator", 
                            args.config.DATASET_PATH, args.config.TEST_ENTITY_MARKER, 
                            args.config.RESULT_ENTITY_MARKER)
            
            
            metrics = utils.get_pubtator_scores("multilingual", args.model, 'valid')
            metrics = {k: float(v) for k, v in metrics.items()}
            wandb.log({'re_precision' : metrics['Precision']} )
            wandb.log({'re_recall' : metrics['Recall']} )
            wandb.log({'re_f1' : metrics['F-score']} )
            return metrics, _, _

    logging.info(f"Training RC model {args.model} model for multilingual train data.")

    df_train = pd.read_csv(f"data_multilingual/train_{args.model}_multilingual_re_dataset.csv")

    df_train.columns = ["doc_id", "text", "labels", "rml_s", "rml_e", "tst_s", "tst_e"]

    df_it = pd.read_csv(f"data_multilingual/valid_{args.model}_it_multilingual_re_dataset.csv")
    df_it.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]
    df_es = pd.read_csv(f"data_multilingual/valid_{args.model}_es_multilingual_re_dataset.csv")
    df_es.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]
    df_eu = pd.read_csv(f"data_multilingual/valid_{args.model}_eu_multilingual_re_dataset.csv")
    df_eu.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]

    # Combine all DataFrames into one
    df_eval  = pd.concat([df_it, df_es, df_eu], ignore_index=True)

    model_config = args.config.model_args_rc 
    optimal_hyperparam_dict = fetch_optimal_hyperparams("rc", args.model, "multilingual")
    model_config.update(optimal_hyperparam_dict)
    # rename wrongly named key.
    model_config['train_batch_size'] = model_config.pop("batch_size")
    model_config['output_dir']  = f"outputs_multilingual/{args.model}_re/"
    model_config['best_model_dir']  = f"models_multilingual/{args.model}_re/"
    model_config['wandb_project'] = f"rc_{args.model}_multilingual_final" 

    model_args = ClassificationArgs()
    model_args.update_from_dict(model_config)

    model_args.labels_list = [0, 1]
    model_args.early_stopping_metric = "F-score"
    model_args.early_stopping_metric_minimize = False


    model = CustomClassificationModel(
        args.model_type, args.model_name, args=model_args
    )

    model.train_model(df_train[["text", "labels"]], 
                      eval_df=df_eval)

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='biobert')
    args = parser.parse_args()
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    model_details = {'mbert': ("bert", "bert-base-multilingual-cased"),
                'xlmroberta': ("xlmroberta", "xlm-roberta-base"), 
                'biobert': ("bert", "dmis-lab/biobert-v1.1"), 
                'bert': ("bert", "bert-base-uncased")}
    configs = Config("multilingual")
    args.config = configs
    args.model_type = model_details[args.model][0]
    args.model_name = model_details[args.model][1]
    Train_RC(args)