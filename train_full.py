"""
Prediction step of the Relation Extraction Task. Combines all the modules.
"""
import argparse
from train_ner import Train_NER
from rc_dataset import RC_Dataset
from train_rc import Train_RC
import secrets
import wandb

from config import Config

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
    parser.add_argument('--use-full-train', default=True, 
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--lang', '-l', default='it')

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]

    args.wandb_key = configs.WANDB_API_KEY
    args.wandb_proj_name = f"{args.lang}_Full_Relation_Extraction"


    configure_wandb(args)

    Train_NER(args)

    args.split = "train"
    RC_Dataset(args)

    Train_RC(args)

