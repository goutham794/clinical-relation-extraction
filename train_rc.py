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

def Train_RC(args):

    class CustomClassificationModel(ClassificationModel):
        def eval_model(self, eval_df, multi_label=False, output_dir=None, verbose=True, silent=False, wandb_log=True, **kwargs):
            predictions, _ = self.predict(list(eval_df.text))
            utils.save_predicted_pubtator(eval_df[np.array(predictions).astype(bool)],args.lang, 
                            f"{args.model}_predicted_valid_set.pubtator", 
                            args.config.DATASET_PATH, args.config.TEST_ENTITY_MARKER, 
                            args.config.RESULT_ENTITY_MARKER)
            
            
            metrics = utils.get_pubtator_scores(args.lang, args.model, 'valid')
            metrics = {k: float(v) for k, v in metrics.items()}
            wandb.log({'re_precision' : metrics['Precision']} )
            wandb.log({'re_recall' : metrics['Recall']} )
            wandb.log({'re_f1' : metrics['F-score']} )
            return metrics, _, _

    logging.info(f"Training RC model {args.model} model for {args.lang} and {'combined' if args.use_full_train else 'split'} train data.")

    df_train = pd.read_csv(f"data_{args.lang}/train_{args.model}_{'full_' if args.use_full_train else ''}re_dataset.csv",
                        #    nrows=100
                           )
    df_train.columns = ["doc_id", "text", "labels", "rml_s", "rml_e", "tst_s", "tst_e"]

    df_eval = pd.read_csv(f"data_{args.lang}/valid_{args.model}_re_dataset.csv",
                        #    nrows=100
                           )
    df_eval.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]

    model_args = ClassificationArgs()
    # model_args.output_dir  = f"outputs_{args.lang}/{args.model}_re/"
    model_args.output_dir  = f"models_{args.lang}/{args.model}_re{'_combined' if args.use_full_train else ''}/"
    # model_args.best_model_dir  = f"models_{args.lang}/{args.model}_re/"
    model_args.use_multiprocessing = False
    model_args.train_batch_size = args.batch_size
    model_args.labels_list = [0, 1]
    model_args.use_multiprocessing_for_evaluation = False
    model_args.evaluate_during_training = True
    model_args.early_stopping_metric = "F-score"
    model_args.early_stopping_metric_minimize = False


    model = CustomClassificationModel(
        args.model_type, args.model_name, args=model_args
    )

    model.train_model(df_train[["text", "labels"]], 
                      eval_df=df_eval)

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument("--batch-size", type=int, default = 16)
    parser.add_argument("--epochs", '-e', type=int, default = 5)
    parser.add_argument('--use-full-train', default=False, 
                        action=argparse.BooleanOptionalAction)
    # parser.add_argument("--lr", default=0.0001, type=float)
    args = parser.parse_args()
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    model_details = {'mbert': ("bert", "bert-base-multilingual-cased"),
                'xlmroberta': ("xlmroberta", "xlm-roberta-base"), 
                'biobert': ("bert", "dmis-lab/biobert-v1.1"), 
                'bert': ("bert", "bert-base-uncased")}
    configs = Config(args.lang)
    args.config = configs
    args.model_type = model_details[args.model][0]
    args.model_name = model_details[args.model][1]
    Train_RC(args)