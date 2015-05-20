# -*- coding: utf-8 -*-
import codecs
import json
import re
import russian
import french


def add_new_text(russian_path, french_path, french_metric_path, russian_metric_path = None,):
    russian.add_new_text(russian_path, russian_metric_path)
    french.add_new_text(french_path, french_metric_path)

def read_data (path):
    data_file = codecs.open(path, 'r', 'utf-8') #Загрузка файла слов
    data = json.load(data_file)
    data_file.close()
    return data


fr_gramm_data = read_data (french.gramm_path)
fr_words_data = read_data (french.words_path)
fr_wordforms_data = read_data (french.wordforms_path)
fr_rythm_data = read_data (french.rythm_path)
fr_strophes_data = read_data (french.strophes_path)
fr_texts_data = read_data (french.texts_path)
	

ru_gramm_data = read_data (russian.gramm_path)
ru_words_data = read_data (russian.words_path)
ru_wordforms_data = read_data (russian.wordforms_path)
ru_rythm_data = read_data (russian.rythm_path)
ru_strophes_data = read_data (russian.strophes_path)
ru_texts_data = read_data (russian.texts_path)

def local_search(data, parameter):
    if parameter in data:
        return data[parameter]
    return []

def local_check(data, parameter):
    return parameter in data

#Как подаются данные на ввод:
#Слово / Характеристики / Позиция_рифмы / Метрика
#Если это не первое слово, то еще расстояние

def form (s_type, lang, words, distances=None, gramm_chars=None, rythms=None):
    symbs = re.compile(u"[!;^:&?*()\-—_+=|/\.,…»«]")
    if s_type == u"ex":
        words = symbs.sub(u"", words)
        words = words.lower().split()
        return strophe_search(lang, exact_form_search(lang, words))
    elif s_type == u"var":
        #gramm_chars = symbs.sub(u"", gramm_chars)
        #gramm_chars = gramm_chars.lower().split()
        for i in range(len(words)):
            words[i] = symbs.sub(u"", words[i])
            words[i] = words[i].lower()
        for i in range(len(rythms)):
            if rythms[i] == -1:
                rythms = False
            elif rythms[i] == 0:
                rythms = None
            elif rythms[i] == 1:
                rythms = True
        return strophe_search(lang, search(lang, words, distances, gramm_chars, rythms))
        


def strophe_search(lang, indexes):
    #print indexes
    strophes_data = []
    texts_data = []
    second_texts_data = []
    if lang == u"russian":
        strophes_data = ru_strophes_data
        texts_data = ru_texts_data
        second_texts_data = fr_texts_data
    elif lang == u"french":
        strophes_data = fr_strophes_data
        texts_data = fr_texts_data
        second_texts_data = ru_texts_data

    texts = []
    prev_index = -1
    words_in_strophe_indexes = []
    for i in indexes:
        result = bin_search(strophes_data, i)
        if result != prev_index:
            prev_index = result
            words_in_strophe_indexes = [i]
            #print strophes_data[result]
            verse = unicode(strophes_data[result][0])
            #print type(verse)
            stanza = unicode(strophes_data[result][1])
            texts.append([texts_data[verse][stanza], second_texts_data[verse][stanza], words_in_strophe_indexes])
        else:
            texts[len(texts)-1][2].append(i)
    russian.write_data("c:\\daniil\\parallel\\s1.json", texts)
    return texts
        

#=====================================================
def dist_search(indexes_1, indexes_2, distance, data):
    #print indexes_1, indexes_2
    result_i_1 = []
    result_i_2 = []
    for i in indexes_1:
        for j in indexes_2:
            if j > i and j <= i + distance:
                if bin_search(data, i) == bin_search(data, j):
                    if i not in result_i_1:
                        result_i_1.append(i)
                    if j not in result_i_2:    
                        result_i_2.append(j)
    #print indexes_1, indexes_2, u":", result_i_1, result_i_2
    return result_i_1, result_i_2


def search(lang, words, distances, gramm_chars, rythms):
    result = []
    for i in xrange(len(words)):
        result.append(pre_search_compile(lang, words[i], gramm_chars[i], rythms[i]))
    strophes_data = []
    if lang == u"russian":
        strophes_data = ru_strophes_data
    elif lang == u"french":
        strophes_data = fr_strophes_data
        
    for i in xrange(len(distances)):
        two_words = result[i:i+2]
        if len(two_words) == 2:
            result[i],result[i+1] = dist_search(two_words[0], two_words[1], distances[i], strophes_data)
    all_indexes = []
    print result
    for i in result:
        all_indexes += i
    #print list(set(all_indexes))
    return sorted(list(set(all_indexes)))


def exact_form_search(lang, words):
    words = words.split()
    distances = [1 for i in range(len(words) - 1)]
    gramm_chars = [[] for i in range(len(words))]
    rythms = [None for i in range(len(words))]
    for i in range(len(words)):
        words[i] = u''.join([u'"', words[i], u'"'])
    return search(lang, words, distances, gramm_chars, rythms)
#=========================================================            
    

def position(index, left, right):
    #print left, right, index
    if index >= left and index <= right:
        return 0
    elif index < left:
        return -1
    elif index > right:
        return 1

def bin_search(data, index):
    mid = len(data)/2
    #print mid
    pos = position(index, data[mid][2], data[mid][3])
    if pos == 0:
        return mid
    elif pos == 1:
        return bin_search(data[mid:], index)
    else:
        return bin_search(data[:mid], index)
    
def strophe_number_search(lang, index):
    data = []
    if lang == "russian":
        data = ru_strophes_data
        pos = data[bin_search(data, index)]
        verse = pos[0]
        stanza = pos[1]
    elif lang == "french":
        data = fr_strophes_data
        pos = data[bin_search(data, index)]
        verse = pos[0]
        stanza = pos[1]
    return verse, stanza
        
        
        

def pre_search_compile(lang, word, stats, is_rythm):
    word_data = {}
    gramm_data = {}
    rythm_data = []
    if lang == "russian":
        if word == word.strip(u'"'):
            word_data = ru_words_data
        else:
            word_data = ru_wordforms_data
        gramm_data = ru_gramm_data
        rythm_data = ru_rythm_data
    elif lang == "french":
        if word == word.strip(u'"'):
            word_data = fr_words_data
        else:
            word_data = fr_wordforms_data
        gramm_data = fr_gramm_data
        rythm_data = fr_rythm_data      
    return index_search(word.strip(u'"'), word_data, stats, gramm_data, is_rythm, rythm_data)
       
def crossing(first, second):
    result = []
    for i in first:
        if i in second:
            result.append(i)
    return result
def no_crossing(first, second):
    result = []
    for i in first:
        if i not in second:
            result.append(i)
    return result

def index_search(word, word_data, stats, gramm_data, is_rythm, rythm_data):
    result = local_search(word_data, word)
    #print result
    for i in stats:
        result = crossing(result, local_search(i, gramm_data))
    if is_rythm == True:
        result = crossing(result, rythm_data)
    elif is_rythm == False:
        result = no_crossing(result, rythm_data)
    return result
