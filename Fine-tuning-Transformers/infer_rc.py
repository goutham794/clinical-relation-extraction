from simpletransformers.classification import ClassificationModel, ClassificationArgs
import argparse
import pandas as pd
import logging
import os
import numpy as np
import wandb
import secrets

from config import Config
import utils

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

def configure_wandb(args):
    wandb.login(key=args.wandb_key)
    wandb.init(
    project=args.wandb_proj_name,
        name = f"{args.model}_{secrets.token_hex(2)}"
        )

def Infer_RC(args):

    df = pd.read_csv(f"data_{args.lang}/{args.split}_{args.model}_re_dataset.csv")
    df.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]

    if args.model == 'rule_based':
        predictions = df.text.apply(utils.classify_relation)
        utils.save_predicted_pubtator(df[predictions], args.lang, 
                                f"{args.model}_predicted_{args.split}_set.pubtator", 
                                args.dataset)
        
        # utils.save_predicted_pubtator(df, args.lang, 
                                # f"{args.model}_predicted_{args.split}_set.pubtator", 
                                # args.dataset)
        # print(utils.get_pubtator_scores(args.lang, args.model, args.split))

    else:
        model_args = ClassificationArgs()
        model_args.use_multiprocessing_for_evaluation = False

        model = ClassificationModel(
            args.model_type, args.model_loc,args=model_args
        )


        predictions, _ = model.predict(list(df.text))

        utils.save_predicted_pubtator(df[np.array(predictions).astype(bool)],args.lang, 
                                f"{args.model}_predicted_{args.split}_set.pubtator", 
                                args.dataset, args.config.TEST_ENTITY_MARKER, 
                                args.config.RESULT_ENTITY_MARKER)
        
        
        metrics = utils.get_pubtator_scores(args.lang, args.model, args.split)
        print(metrics)
        wandb.log({"re_precision": float(metrics['Precision'])})
        wandb.log({"re_recall": float(metrics['Recall'])})
        wandb.log({"re_f1_score": float(metrics['F-score'])})
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument('--model', '-m', default='biobert')
    parser.add_argument('--split', '-s', default='test')
    args = parser.parse_args()
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert', 'rule_based'], "The model must be one of bert, xlmroberta, biobert"

    configs = Config(args.lang)
    args.config = configs
    
    args.model_type = configs.pretrained_model_details[args.model][0]
    # args.model_loc = f"models_{args.lang}/{args.model}_rc{'_combined' if args.split!='valid' else ''}"
    args.model_loc = f"models_{args.lang}/{args.model}_rc"
    
    if args.split == 'test':
        args.dataset = args.config.TEST_DATASET 
    else:
        args.dataset = args.config.DATASET_PATH  

    args.wandb_key = configs.WANDB_API_KEY
    args.wandb_proj_name = f"Infer_RC_{args.lang}_Relation_Extraction"
    configure_wandb(args)


    Infer_RC(args)