# -*- coding: utf-8 -*-
import codecs
import re
import os
import json

data = {} #словарь обратных индексов грамматических характеристик
words = {} #словарь обратных индексов точных форм
wordforms = {} #словарь обратных индексов словоформ

def mystem_parcing(input_path, output_path, mystem_dir="C:\\daniil\\mystem.exe", options="-n -d -e cp1251 -i --eng-gr"): #Парсинг текстов
    os.system(mystem_dir + " " + options + " " + input_path + " " + output_path) #c:\\daniil\\text.txt c:\\daniil\\res2.txt")
#mystem_parcing(u"c:\\daniil\\text1.txt", u"c:\\daniil\\parced_ru1.txt")


def def_stats(stats, index): #Выделение грамматических характеристик. Проблема омонимии решена майстемовскими средствами, но, к сожалению, не на все 100%
    gram_char = re.compile(u'[a-z0-9]*', flags = re.U)
    omonims = gram_char.findall(stats)
    for i in omonims:
        if i != u'':
            if i in data:
                if index not in data[i]:
                    data[i].append(index)
            else:
                data.update({i:[index]})

def def_words(word, wordform, index): #выделение точной и словоформы
    if word in words:
        if index not in words[word]:
            words[word].append(index)
    else:
        words.update({word:[index]})

    if wordform in wordforms:
        if index not in wordforms[wordform]:
            wordforms[wordform].append(index)
    else:
        wordforms.update({wordform:[index]})



def create_data(parced_path): #создание словарей обратных индексов
    parcer_info = re.compile(u'{.*}', flags = re.U)
    word_info = re.compile(u'[а-яА-Я]*')
    
    parced_file = codecs.open(parced_path, 'r', 'cp1251') #"C:\\daniil\\res.txt"
    index = 0
    for i in parced_file:
        stats = parcer_info.findall(i)[0]
        def_stats(stats, index)

        words = word_info.findall(i)
        word = words[0].lower()
        wordform = words[2]
        def_words(word, wordform, index)   
        
        index += 1
        
    parced_file.close()
   



create_data(u"C:\\daniil\\parced_ru1.txt") #на вход подается файл, полученный из майстема

##Пока что создается три файла json: грамм. характеристики, точные формы, словоформы.
a = codecs.open(u"c:\\daniil\\result_data.json", u"w", u"cp1251")
json.dump(data, a, indent = 1)
a.close()

a = codecs.open(u"c:\\daniil\\result_words.json", u"w", u"utf-8")
json.dump(words, a, indent = 1)
a.close()

a = codecs.open(u"c:\\daniil\\result_wordforms.json", "w", "cp1251")
json.dump(wordforms, a, indent = 1)
a.close()
