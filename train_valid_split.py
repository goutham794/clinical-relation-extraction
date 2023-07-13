import os
import config
import random

random.seed(42)

documents_folder = config.TOKEN_DATA_PATH

doc_ids = os.listdir(documents_folder)

doc_ids = [x[:-4] for x in doc_ids]

print(random.sample(doc_ids, int(0.15 * len(doc_ids))))





