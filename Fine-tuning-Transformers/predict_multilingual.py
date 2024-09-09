"""
Prediction step of the Relation Extraction Task. Combines all the modules.
"""
import argparse
from infer_ner_multilingual import Infer_NER
from rc_dataset_multilingual import RC_Dataset
from infer_rc_multilingual import Infer_RC
import wandb
import secrets

from config import Config

def configure_wandb(args):
    wandb.login(key=args.wandb_key)
    wandb.init(
    project=args.wandb_proj_name,
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

    args.wandb_key = configs.WANDB_API_KEY
    args.wandb_proj_name = f"{args.lang}_test_Relation_Extraction"
    configure_wandb(args)

    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]
    args.split = "test"

    Infer_NER(args)

    RC_Dataset(args)

    args.model_loc = f"models_multilingual/{args.model}_re_combined"
    args.dataset = args.config.TEST_DATASET 
    Infer_RC(args)
