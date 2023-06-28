from simpletransformers.ner import NERModel,NERArgs
import argparse
import os
import logging

from config import Config

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def Train_NER(args):

    logging.info(f"Training NER model {args.model} model and {'combined' if args.use_full_train else 'split'} train data.")

    model_config = args.config.model_args_ner 
    model_config['train_batch_size'] = args.batch_size
    model_config['output_dir']  = f"outputs_{args.lang}/{args.model}_ner/"
    model_config['best_model_dir']  = f"models_{args.lang}/{args.model}_ner{'_combined' if args.use_full_train else ''}/"
    # model_config['learning_rate']  = args.lr
    model_config['num_train_epochs']  = args.epochs

    model_args = NERArgs()
    model_args.update_from_dict(model_config)

    custom_labels = args.config.NER_CLASSES

    model = NERModel(
        args.model_type, args.model_name, args=model_args, labels=custom_labels
    )

    model.train_model(f"data_{args.lang}/train{'_full' if args.use_full_train else ''}.txt", 
                      eval_data=f"data_{args.lang}/valid.txt"
                      )

    # Evaluate the model
    result, model_outputs, predictions = model.eval_model(f"data_{args.lang}/valid.txt")


    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='xlmroberta')
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
    args.config = configs
    args.model_type = configs.pretrained_model_details[args.model][0]
    args.model_name = configs.pretrained_model_details[args.model][1]
    Train_NER(args)