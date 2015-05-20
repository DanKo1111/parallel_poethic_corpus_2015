# -*- coding: utf-8 -*-
import codecs
import re
import os
import json

gramm_path = u"ru_data_gramm.json"
words_path = u"ru_data_words.json"
wordforms_path = u"ru_data_wordforms.json"
rythm_path = u"ru_data_rythm.json"
strophes_path = u"ru_data_strophes.json"
texts_path = u"ru_data_texts.json"
length_path = u"ru_data_length.json"


def clear_corpora():
    write_data (gramm_path, {})
    write_data (words_path, {})
    write_data (wordforms_path, {})
    write_data (rythm_path, [])
    write_data (strophes_path, [])
    write_data (texts_path, {})
    write_data (length_path, 0)
##    write_data (rhyme_path, {})
##    write_data (caesura_path, {})

def read_data (path):
    data_file = codecs.open(path, 'r', 'utf-8') #Загрузка файла слов
    data = json.load(data_file)
    data_file.close()
    return data

def write_data (path, data):
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'utf-8')
    json_file.write (json_data)
    json_file.close()

    
#Берем текст (пример - final_ru.txt), и готовим его к пропуску через майстем
def text_preparcing(text_path): #что бы текст можно было нормально пропустить через майстем, надо убрать все лишнее. 
    text_file = codecs.open(text_path, 'r', 'utf-8')
    preparced_text = u"" 
    for i in text_file:
        if i[0] != u"<" and i[1] != u"<":
            preparced_text += i
    text_file.close()
    new_path = text_path[:-4] + u"_preparced.txt"
    new_file = codecs.open(new_path, 'w', "utf-8")
    new_file.write(preparced_text)
    new_file.close()
    return new_path

def mystem_parcing(input_path, output_path, mystem_dir="C:\\daniil\\mystem.exe", options="-n -d -e utf-8 -i --eng-gr"): #Парсинг текстов
    os.system(mystem_dir + " " + options + " " + input_path + " " + output_path)



def def_stats(stats, index, gram_data): #Выделение грамматических характеристик. Проблема омонимии решена майстемовскими средствами, но, к сожалению, не на все 100%
    gram_char = re.compile(u'[a-z0-9]*', flags = re.U)
    omonims = gram_char.findall(stats)
    for i in omonims:
        if i != u'':
            if i in gram_data:
                if index not in gram_data[i]:
                    gram_data[i].append(index)
            else:
                gram_data.update({i:[index]})
    return gram_data

def def_words(word, wordform, index, words, wordforms): #выделение точной формы и словоформы
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
    return words, wordforms

def create_parcing_data(parced_path): #создание словарей обратных индексов
    parcer_info = re.compile(u'{.*}', flags = re.U)
    word_info = re.compile(u'[а-яА-Я][а-яА-Я]*')
    parced_file = codecs.open(parced_path, 'r', 'utf-8')

    words = read_data(words_path)
    wordforms = read_data(wordforms_path)
    gramm = read_data(gramm_path)
    
    index = read_data(length_path) - 1
    if index > 0:
        index += 1
    for i in parced_file:
        index += 1
        i = i.lower()
        stats = parcer_info.findall(i)[0]
        if stats:
            gramm = def_stats(stats, index, gramm)
        
        parced_words = word_info.findall(i)
        if parced_words:
            wordform = parced_words[0].lower()
            word = parced_words[1]
            words, wordforms = def_words(word, wordform, index, words, wordforms)        
        #index += 1
    
    write_data(gramm_path, gramm)
    write_data(words_path, words)
    write_data(wordforms_path, wordforms)
    parced_file.close()
    print u"CPD: ", index

def is_word(word): #А слово ли word?...
    return bool(re.findall(u"[А-Яа-я][А-Яа-я]*", word))

def create_rythm_data(preparced_text_path): 
    text_file = codecs.open(preparced_text_path, 'r', 'utf-8')
    delete_symb = re.compile(u'[…()",\.?!:;\-—»«]', flags = re.U)
    rythm_index = read_data(rythm_path)
    index = read_data(length_path) - 1
    
    for i in text_file: #Тут создается массив с индексами позиций рифм
        for j in delete_symb.sub(u"", i).split():
            if is_word(j):
                index += 1
        rythm_index.append(index) #Тут он заканчивает создаваться
    write_data(rythm_path, rythm_index)
    print u"CRD: ", index

def create_text_data(text_path): #Создание контекстной датабазы
    text_file = codecs.open(text_path, 'r', 'utf-8')
    text = text_file.read()
    splited_text = text.split(u"<")
    write_data(length_path, create_stanza_data(splited_text))   
    text_file.close()

def create_stanza_data(splited_text): #Индексные границы строф. Универсальная.

    strophe_index = read_data(strophes_path)
    text_data = read_data(texts_path)
    
    verse_index = 0
    stanza_index = 0
    index = read_data(length_path) - 1
    begin = 0
    end = 0

    stanza_marker = re.compile("[0-9][0-9]*:[0-9][0-9]*>")
    get_nums = re.compile(u">")

    for i in splited_text:
        is_stanza = stanza_marker.findall(i)
        if is_stanza:
            vers_stanz_data = get_nums.sub(u"", is_stanza[0])
            vers_stanz_data = vers_stanz_data.split(u":")
            verse_index = int(vers_stanz_data[0])
            stanza_index = int(vers_stanz_data[1])
            strophe_text = stanza_marker.sub(u"", i)
            next_len = 0
            for j in strophe_text.split():
                if is_word(j):
                    next_len += 1
            begin = index
            end = index + next_len - 1
            index = end + 1
            strophe_index.append([verse_index, stanza_index, begin, end])

            if verse_index in text_data:
                text_data[verse_index].update({stanza_index:strophe_text})
            else:
                text_data.update({verse_index:{stanza_index:strophe_text}})
    write_data(strophes_path, strophe_index)
    write_data(texts_path, text_data)
    print u"CSD:", index
    return index

def add_new_text(new_text_path, metric_path=None):
    preparced_text_path = text_preparcing(new_text_path)
    parced_text_path = preparced_text_path[:-14] + u"_parced.txt"
    mystem_parcing(preparced_text_path, parced_text_path)

    create_parcing_data(parced_text_path)
    create_rythm_data(preparced_text_path)
    create_text_data(new_text_path)
