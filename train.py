"""
Training of the Relation Extraction Task. Combines all the modules.
"""
import wandb
import secrets
import argparse
import os

from train_ner import Train_NER
from infer_ner import Infer_NER
from rc_dataset import RC_Dataset
from train_rc import Train_RC
from infer_rc import Infer_RC

from config import Config

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def configure_wandb(args):
    wandb.login(key=args.wandb_key)
    wandb.init(
    project=args.wandb_proj_name,
        config={"epochs": args.epochs, "batch_size": args.batch_size, 
                "lr": args.lr}, 
        name = f"{args.model}_{secrets.token_hex(2)}"
        )


if __name__ == "__main__":
    

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--use-full-train', default=False, 
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument("--batch-size", type=int, default = 16)
    parser.add_argument("--epochs", '-e', type=int, default = 5)
    parser.add_argument("--lr", default=0.0001, type=float)

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"

    configs = Config(args.lang)
    args.wandb_key = configs.WANDB_API_KEY
    args.wandb_proj_name = f"{args.lang}_Relation_Extraction"


    configure_wandb(args)

    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]
    Train_NER(args)
    args.split = "valid"
    Infer_NER(args)
    

    args.split = "train"
    args.use_full_train = False
    RC_Dataset(args)

    args.split = "valid"
    RC_Dataset(args)

    Train_RC(args)

    # args.model_loc = f"models_{args.lang}/{args.model}_re"
    # args.dataset = args.config.DATASET_PATH  
    # Infer_RC(args)
