from pymystem3 import Mystem
import rusyllab


def read_text(filename):
    '''Функция читает файл с текстом
    filename -- имя файла'''
    with open(filename, encoding='utf-8') as file:
        text = file.read()
        return text.lower()


def save_file(filename, result):
    '''Функция сохраняет префиксное дерево с разбором в файл'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(result))


def add_to_tree(word, value, tree):
    '''Функция добавляет слово в дерево'''
    def add_node(syllable, level):
        if syllable not in level:
            level[syllable] = {}
        return level[syllable]
    sylls = word.split('|')
    l = tree
    for syll in sylls:
        l = add_node(syll, l)
    l['analysis'] = value
    return tree


def take_analysis(word, tree):
    '''Функция ищет слово в дереве и возвращает его морфологический разбор'''
    def finde_value(syllable, level):
        if syllable in level:
            return level[syllable]
        else:
            return None
    sylls = word.split('|')
    for syll in sylls:
        tree = finde_value(syll, tree)
        if not tree:
            return None
    value = tree['analysis']
    return value


def main():
    m = Mystem()
    # text = read_text('borodino.txt')
    text = 'сколько сейчас времени?'  # текст, анализ которого проводим и засовываем в дерево
    analysis = m.analyze(text)
    pref_tree = {}
    for word in analysis:
        if 'analysis' in word:
            pref_tree = add_to_tree('|'.join(rusyllab.split_word(word['text'])), word['analysis'][0], pref_tree)
    word_analysis = 'времени'  # слово, анализ которого надо найти в дереве
    morph = take_analysis('|'.join(rusyllab.split_word(word_analysis)), pref_tree)
    # save_file('result.txt', pref_tree)
    print(pref_tree)
    print(morph)


if __name__ == '__main__':
    main()
