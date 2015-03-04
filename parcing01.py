# -*- coding: utf-8 -*-
import codecs
import re
import os

class data: #Данные о слове
    def __init__(self, word, wordform, grammar_options, positions):
        self.word = word #Слово
        self.wordform = wordform #Словоформа
        self.grammar_options = options #Массив (ну или какая-нибудь другая форма хранения данных, если я ее придумаю) грамматических опций слова
        self.positions = positions #Массив номеров слов с одинаковыми word, wordform, options

class stanza: #Данные о строфе
    def __init__(self, verse_number, stanza_number, stanza_text, left_index, right_index):
        self.verse_number = verse_number #Номер стиха
        self.stanza_number = stanza_number #Номер строфы
        self.stanza_text = stanza_text #массив элементов с типом data
        self.right_index = right_index #порядковый номер первого слова строфы
        self.left_index = left_index #порядковый номер последнего слова строфы
    def show_strophe():
        return self.stanza_text
    def show_verse_number():
        return verse_number
    def show_stanza_number():
        return stanza_number
    def show_range():
        return [left_index, right_index]

class corpora(data): #А тут должен быть корпус. С обработкой всякого. НО... его тут пока нет
    def __init__(self, texts):
        self.texts = texts
    def in_words(request): #Тут должен быть запрос в корпус. По всем параметрам. 
        for i in texts:
            if request == i.word:
                return i #
    def in_wordforms(request):
            pass
    #...

def mystem_parcing(input_path, output_path, mystem_dir="C:\\daniil\\mystem.exe", options="-n -e cp1251 -i"):
    os.system(mystem_dir + " " + options + " " + input_path + " " + output_path) #c:\\daniil\\text.txt c:\\daniil\\res2.txt")

def strophes_index(): 
    pass

##А дальше почти ничего не изменилось

def create_data(parced_path):
    strophe_number = re.compile(u'<\d:\d>', flags = re.U) #Поиск номера стиха в номере файла
    parcer_info = re.compile(u'{.*}', flags = re.U)
    parced_file = codecs.open(parced_path, 'r', 'cp1251') #"C:\\daniil\\res.txt"
    texts = []
    index = 0
    verse = u""
    stanza = u""
    for i in parced_file:
        new_word = data()
        if strophe_number.findall(i):
            new_word


        word = parcer_info.sub('', i).strip()
        parameters = parcer_info.findall(i)[0] #Вообще, вот тут параметры надо как-то разбирать из строки в какой-то формальный вид. Но я еще не придумал, как. 
        data.append([word, parameters])
    for i in data:
        for j in i:
            print j
        print "---------------------------"
