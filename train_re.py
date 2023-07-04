from simpletransformers.classification import ClassificationModel, ClassificationArgs
import argparse
import pandas as pd
import logging
import os
import numpy as np

from config import Config
import utils

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def Train_RE(args):

    logging.info(f"Training RE model {args.model} model for {args.lang} and {'combined' if args.use_full_train else 'split'} train data.")

    df_train = pd.read_csv(f"data_{args.lang}/train_{args.model}_{'full_' if args.use_full_train else ''}re_dataset.csv")
    df_train.columns = ["doc_id", "text", "labels", "rml_s", "rml_e", "tst_s", "tst_e"]

    # df_eval = pd.read_csv(f"data_{args.lang}/valid_re_dataset.csv")
    # df_eval.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]

    model_args = ClassificationArgs()
    model_args.num_train_epochs = args.epochs
    model_args.manual_seed = 42
    model_args.overwrite_output_dir =True
    # model_args.output_dir  = f"outputs_{args.lang}/{args.model}_re/"
    model_args.output_dir  = f"models_{args.lang}/{args.model}_re{'_combined' if args.use_full_train else ''}/"
    # model_args.best_model_dir  = f"models_{args.lang}/{args.model}_re/"
    model_args.use_multiprocessing = False
    model_args.train_batch_size = args.batch_size
    model_args.labels_list = [0, 1]
    model_args.use_multiprocessing_for_evaluation = False
    # model_args.evaluate_during_training = True


    model = ClassificationModel(
        args.model_type, args.model_name, args=model_args
    )

    model.train_model(df_train[["text", "labels"]])

    # predictions, _ = model.predict(list(df_eval.text))

    # utils.save_predicted_pubtator(df_eval[np.array(predictions).astype(bool)], 
    #                               args.lang, f"{args.model}_predicted_valid_set.pubtator", 
    #                         args.config.DATASET_PATH)

        

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
    if args.use_full_train: assert args.split == 'train'
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    model_details = {'mbert': ("bert", "bert-base-multilingual-cased"),
                'xlmroberta': ("xlmroberta", "xlm-roberta-base"), 
                'biobert': ("bert", "dmis-lab/biobert-v1.1"), 
                'bert': ("bert", "bert-base-uncased")}
    configs = Config(args.lang)
    args.config = configs
    args.model_type = model_details[args.model][0]
    args.model_name = model_details[args.model][1]
    Train_RE(args)