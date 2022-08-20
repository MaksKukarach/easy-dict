import requests
from bs4 import BeautifulSoup

def get_word_set_from_oxford(word, include_examples=True):
    response = get_word_page_from_oxford(word)

    word_set = WordSet()

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        headword = soup.find('h1', class_='headword')
        word_set.word = headword.text

        definition = soup.find('span', class_='def')
        word_set.definition = definition.text

        if include_examples:
            examples_ul = soup.find('ul', class_='examples')
            examples = examples_ul.find_all('span', class_='x')

            if len(examples) > 3: examples = examples[:3]
            
            word_set.examples = [ex.text for ex in examples]        
    else:
        word_set.word = word

    return word_set

def get_word_page_from_oxford(word):
    url = f'https://www.oxfordlearnersdictionaries.com/definition/english/{word}_1?q={word}+'

    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    response = requests.get(url, headers=headers)
    return response

def modify_examples(word_set):
        examples = word_set.examples

        if examples != '':
            word = word_set.word
            for i in range(len(examples)):
                lst = examples[i].split()
                for j, w in enumerate(lst):
                    if word in w and len(w) <= len(word) + 2:
                        lst[j] = w.replace(word, '_' * len(word))

                examples[i] = ' '.join(lst)

        word_set.examples = examples

        return word_set

def add_word_set_to_quizlet(word_set):
    pass

class WordSet:
    word = str
    definition = str
    examples = str

    def __init__(self, word: str = 'undefined', definiton: str = 'undefined', examples: str = '') -> None:
        self.word = word
        self.definition = definiton
        self.examples = examples


    def __str__(self) -> str:
        return f"{self.word} - {self.definition}. {self.examples}"