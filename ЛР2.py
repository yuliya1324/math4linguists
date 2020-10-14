import re
import collections
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)


def find_natasha(text):
    '''Функция, которая находит организации и адреса в статье'''
    # создадим множества организация и адресов, чтобы они не повторялись
    orgs = set()
    locs = set()
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)
    for word in doc.spans:
        word.tokens[-1].lemmatize(morph_vocab)
        # Если организация, то добавляем к множеству организаций
        if word.type == 'ORG':
            orgs.add(word.tokens[-1].lemma)
        # Если адрес, то добавляем к множеству адресов
        elif word.type == 'LOC':
            locs.add(word.tokens[-1].lemma)
    return orgs, locs


def take_article(filename):
    '''Функция, которая достает статьи из файла'''
    with open(filename, encoding='utf-8') as file:
        text = file.read()
        articles = re.findall('-\n(.+\n.+)\n=', text)
        return articles


def get_org(articles):
    '''Функция, которая строит граф связей организаций и адресов'''
    # Граф будет в виде {Организация: {Адрес: количество общих статей}}
    organizations = collections.defaultdict(lambda: collections.defaultdict(int))
    for article in articles:
        orgs, locs = find_natasha(article)
        for org in orgs:
            for loc in locs:
                organizations[org][loc] += 1
    return organizations


def find_adress(organizations):
    '''Функция выбирает наиболее вероятный адрес каждой организации'''
    new_connects = {}
    for org in organizations:
        m = 0
        m_loc = False
        for loc in organizations[org]:
            # выбираем тот адрес, который чаще всего встречается с данной организацией и при этом не менее 5 раз
            if organizations[org][loc] > m and organizations[org][loc] > 5:
                m = organizations[org][loc]
                m_loc = loc
        if m_loc:
            # оздаем словарь, в котором каждому значению организации соответствует ее наиболее вероятный адрес
            # и количесвто общих статей
            new_connects[org] = (m_loc, m)
    return new_connects


def main():
    articles = take_article('news.txt')
    connects = get_org(articles)
    print(find_adress(connects))


if __name__ == '__main__':
    main()
