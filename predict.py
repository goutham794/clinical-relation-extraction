"""
Prediction step of the Relation Extraction Task. Combines all the modules.
"""
import argparse
from train_ner import Train_NER
from infer_ner import Infer_NER
from rc_dataset import RC_Dataset
from train_rc import Train_RC
from infer_rc import Infer_RC

from config import Config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='mbert')
    parser.add_argument('--use-full-train', default=True, 
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--lang', '-l', default='it')
    parser.add_argument("--batch-size", type=int, default = 16)
    parser.add_argument("--epochs", '-e', type=int, default = 5)
    parser.add_argument("--lr", default=0.0001, type=float)

    args = parser.parse_args()
    assert args.lang in ['it', 'es', 'eu'], "The language must be one of 'it', 'es', 'eu'"
    assert args.model in ['mbert', 'xlmroberta', 'biobert','bert'], "The model must be one of bert, xlmroberta, biobert"
    configs = Config(args.lang)
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]
    args.split = "test"

    Infer_NER(args)

    RC_Dataset(args)

    args.model_loc = f"models_{args.lang}/{args.model}_re_combined"
    args.dataset = args.config.TEST_DATASET 
    Infer_RC(args)
