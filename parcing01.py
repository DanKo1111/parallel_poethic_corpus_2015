# -*- coding: utf-8 -*-
import codecs
import re
import os
import json

data = {} #Словарь обратных индексов грамматических характеристик. Формат: {ХАРАКТЕРИСТИКА:[ИНДЕКСЫ], ...}
words = {} #Словарь обратных индексов точных форм. Формат: {СЛОВО:[ИНДЕКСЫ], ...}
wordforms = {} #Словарь обратных индексов словоформ. Формат: {СЛОВОФОРМА:[ИНДЕКСЫ], ...}
rythm_index = [] #Индексы позиций рифм. Формат: [ИНДЕКСЫ]
strophe_index = [] #Какой строфе какие индексы принадлежат. Формат: {[СТИХ, СТРОФА]:[НАЧАЛЬНЫЙ_ИНДЕКС, КОНЕЧНЫЙ_ИНДЕКС], ...}


def text_preparcing(text_path): #что бы текст можно было нормально пропустить через майстем, надо убрать все лишнее. 
    text_file = codecs.open(text_path, 'r', 'utf-8')
    preparced_text = u"" 
    for i in text_file:
        if i[0] != u"<" and i[1] != u"<":
            preparced_text += i
    text_file.close()
    new_file = codecs.open(text_path[:-4] + u"_preparced.txt", 'w', "cp1251")
    new_file.write(preparced_text)
    new_file.close()
##text_preparcing(u"C:\\daniil\\final_ru.txt")

def mystem_parcing(input_path, output_path, mystem_dir="C:\\daniil\\mystem.exe", options="-n -d -e cp1251 -i --eng-gr"): #Парсинг текстов
    os.system(mystem_dir + " " + options + " " + input_path + " " + output_path) #c:\\daniil\\text.txt c:\\daniil\\res2.txt")
##mystem_parcing(u"c:\\daniil\\final_ru_preparced.txt", u"c:\\daniil\\parced1_ru.txt")


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

def def_words(word, wordform, index): #выделение точной формы и словоформы
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


def is_word(word): #А слово ли word?...
    return bool(re.findall(u"[а-яА-Я]", word))

def create_rythm_data(preparced_text_path): 
    text_file = codecs.open(preparced_text_path, 'r', 'cp1251')
    index = -1
    for i in text_file: #Тут создается массив с индексами позиций рифм
        for j in i.split():
            if is_word(j):
                index += 1
        rythm_index.append(index) #Тут он заканчивает создаваться
    
##create_rythm_data(u"C:\\daniil\\final_ru_preparced.txt")



##def create_stanza_data(text_path):
##    text_file = codecs.open(text_path, 'r', 'utf-8')
##    text = text_file.read()
##    
##    verse_index = 0
##    stanza_index = 0
##    index = -1
##    begin = 0
##    end = 0
##    
##    index_marker = re.compile("<.*>")
##    is_stanza = False
##    for i in text.split():
##        marker = index_marker.findall(i)
##        if bool(marker) and not u"n" in marker:
##            is_stanza = True
##            end = index
##
##            strophe_index.append([verse_index, stanza_index, begin, end])
##
##            
##            verse_index = marker[0][1]
##            stanza_index = marker[0][3]
##            begin = index + 1
##
##            
##        elif u"n" in marker:
##            is_stanza = False
##        elif is_stanza and is_word(i):
##            index += 1
##    text_file.close()
##create_stanza_data(u"C:\\daniil\\final_ru.txt")
##for i in strophe_index:
##    print i
                    
            
##create_stanza_data()


def create_parcing_data(parced_path): #создание словарей обратных индексов
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
    
##create_parcing_data(u"C:\\daniil\\parced1_ru.txt") #на вход подается файл, полученный из майстема



##Пока что создается три файла json: грамм. характеристики, точные формы, словоформы.
##a = codecs.open(u"c:\\daniil\\result_data.json", u"w", u"cp1251")
##json.dump(data, a, indent = 1)
##a.close()
##
##a = codecs.open(u"c:\\daniil\\result_words.json", u"w", u"utf-8")
##json.dump(words, a, indent = 1)
##a.close()
##
##a = codecs.open(u"c:\\daniil\\result_wordforms.json", "w", "cp1251")
##json.dump(wordforms, a, indent = 1)
##a.close()
##
##a = codecs.open(u"c:\\daniil\\result_rythms.json", "w", "cp1251")
##json.dump(rythm_index, a, indent = 1)
##a.close()
