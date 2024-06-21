from typing import List

def read_data(lang: str, split: str = 'train'):
    # Open and read the file
    with open(f'data_{lang}/{split}.txt', 'r') as file:
        content = file.read()

    return content.split('\n\n')



def write_multilingual_data(split: str = 'train'):

    italian_data = read_data('it', split=split)
    spanish_data = read_data('es', split=split)
    basque_data = read_data('eu', split=split)

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