import requests
from bs4 import BeautifulSoup

def oxford_to_quizlet(word: str, first_def_only: bool=True, first_examples_only: bool=True):
    """
    The main function that does the whole process of parsing word and its definition(s)
    from oxford dictionary to quizlet.

    Args:
        word (str) - target word
        first_def_only (bool=True) - if True, will parse only the first definition
        first_examples_only (bool=True) - if True, will parse only first 3 examples

    Returns a WordSet object which can be printed right away.
    """
    word_set = get_word_set_from_oxford(word, first_def_only, first_examples_only)
    word_set = modify_examples(word_set)
    add_word_set_to_quizlet(word_set)
    return word_set

def get_word_set_from_oxford(word, first_def_only=True, first_examples_only=True):
    response = get_word_page_from_oxford(word)

    word_set = WordSet()
    word_set.word = word

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        if first_def_only:
            definition = soup.find('span', class_='def').text
            word_set.definitions.append(definition)

            examples_ul = soup.find('ul', class_='examples')
            if examples_ul is not None:
                examples = examples_ul.find_all('span', class_='x')

                if first_examples_only:
                    if len(examples) > 3: examples = examples[:3]

                word_set.examples.append([ex.text for ex in examples])
        else:
            pass
    return word_set

def modify_examples(word_set):
    """
    Replaces the target word in examples with a line as such: bananas -> '______s'
    """
    target_word = word_set.word

    for i, ex_list in enumerate(word_set.examples):
        for j in range(len(ex_list)):
            ex_list[j] = ex_list[j].replace(target_word, '_'*len(target_word))

        word_set.examples[i] = ex_list

    return word_set

def add_word_set_to_quizlet(word_set):
    pass

def get_word_page_from_oxford(word: str):
    word = word.lower()
    url = f'https://www.oxfordlearnersdictionaries.com/definition/english/{word}_1?q={word}+'

    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    response = requests.get(url, headers=headers)
    return response

class WordSet:
    def __init__(self) -> None:
        self.word = 'undefined'
        self.definitions = list()
        self.examples = list()

    def __str__(self) -> str:
        for i in range(len(self.definitions) - len(self.examples)):
            self.examples.append([''])
        def_ex_map = str([i for i in zip(self.definitions, self.examples)])
        return f"{self.word} - {def_ex_map.replace('[', '').replace(']', '')[1:-1]};"