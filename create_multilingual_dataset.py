from typing import List
import random

def read_data(lang: str, split: str = 'train'):
    # Open and read the file
    with open(f'data_{lang}/{split}.txt', 'r') as file:
        content = file.read()

    return content.split('\n\n')



def write_multilingual_data(split: str = 'train'):

    italian_data = read_data('it', split=split)
    spanish_data = read_data('es', split=split)
    basque_data = read_data('eu', split=split)

    if split == 'train':
        len_italian = len(italian_data)
        len_spanish = len(spanish_data)
        len_basque = len(basque_data)
        print(len_italian)
        print(len_spanish)
        print(len_basque)
        max_length = max(len_italian, len_spanish, len_basque)
    
        def extend_data(data, target_length):
            extension_length = target_length - len(data)
            extended_data = data + random.sample(data, min(extension_length, len(data)))
            extension_length = target_length - len(extended_data)
            return extended_data + random.sample(extended_data, extension_length)

        italian_data = extend_data(italian_data, max_length)
        spanish_data = extend_data(spanish_data, max_length)
        basque_data = extend_data(basque_data, max_length)

    print(len(italian_data))
    print(len(spanish_data))
    print(len(basque_data))


    for it_d, es_d, eu_d in zip(italian_data, spanish_data, basque_data):
        it_d = "[IT] O\n" + it_d + "\n\n"
        es_d = "[ES] O\n" + es_d + "\n\n"
        eu_d = "[EU] O\n" + eu_d + "\n\n"
        with open(f"data_multilingual/{split}.txt", 'a+') as file:
            file.write(it_d)
            file.write(es_d)
            file.write(eu_d)

if __name__ == "__main__":
    write_multilingual_data('train')
    write_multilingual_data('valid')