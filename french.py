# -*- coding: utf-8 -*-
import codecs
import re
import os
import json


gramm_path = u"fr_data_gramm.json"
words_path = u"fr_data_words.json"
wordforms_path = u"fr_data_wordforms.json"
rythm_path = u"fr_data_rythm.json"
strophes_path = u"fr_data_strophes.json"
texts_path = u"fr_data_texts.json"
length_path = u"fr_data_length.json"


def clear_corpora():
    write_data (gramm_path, {})
    write_data (words_path, {})
    write_data (wordforms_path, {})
    write_data (rythm_path, [])
    write_data (strophes_path, [])
    write_data (texts_path, {})
    write_data (length_path, 0)
    

#data_files = [gramm_path, words_path, wordforms_path, rythm_path, strophes_path, texts_path, verses_path]

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


def text_preparcing(text_path): #что бы текст можно было нормально пропустить через майстем, надо убрать все лишнее. 
    remove_symb = re.compile(u"[\"«»—+-.,!?()=;:]")
    text_file = codecs.open(text_path, 'r', 'utf-8')
    preparced_text = u"" 
    for i in text_file:
        if i[0] != u"<" and i[1] != u"<":
            cl_text = remove_symb.sub(u"", i)
            for j in cl_text.split():
                preparced_text = (preparced_text + j + u"\n").lower()
    
    text_file.close()
    new_path = text_path[:-4] + u"_preparced.txt"
    new_file = codecs.open(new_path, 'w', "utf-8")
    new_file.write(preparced_text)
    new_file.close()
    return new_path

def new_file(path, coding="utf-8"):
    new = codecs.open(path, "w", coding)
    new.close()

def treetagger_parcing (input_path, output_path, language="french"):
    #new_file(output_path)
    os.system("set PATH=C:\TreeTagger\bin;%PATH%")
    os.system("cd c:\TreeTagger")
    os.system("tag-" + language + " " + input_path + " " + output_path)
    #os.system("cd c:\TreeTagger")
    #os.system("tag-" + language + " " + input_path + " " + output_path)

#treetagger_parcing (r"c:\Daniil\parallel_corpora\final_fr_preparced.txt", r"c:\Daniil\parallel_corpora\final_fr_parced.txt", "french")

#=============================================

def def_stats(stats, index, data): #Выделение грамматических характеристик. Проблема омонимии решена майстемовскими средствами, но, к сожалению, не на все 100%
    if stats in data:
        data[stats].append(index)
    else:
        data.update({stats:[index]})
    return data
    
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

def create_parcing_data(parced_path):
    parced_file = codecs.open(parced_path, 'r', 'utf-8')

    words = read_data(words_path)
    wordforms = read_data(wordforms_path)
    gramm = read_data(gramm_path)

    index = read_data(length_path)

    
    for i in parced_file:
        data_split = i.split()
        #print data_split
        wordform = data_split[0]
        word = data_split[2]
        stats = data_split[1]
        gramm = def_stats(stats, index, gramm)
        #print word, " ", wordform
        words, wordforms = def_words(word, wordform, index, words, wordforms)
        index += 1
    write_data(gramm_path, gramm)
    write_data(words_path, words)
    write_data(wordforms_path, wordforms)
    #print index
    parced_file.close()

#==============================================
def france_text_len(text, wordforms):
    delete_symb = re.compile(u'[…()",\.?!:;\-—»«]', flags = re.U)
    text = delete_symb.sub(u'', text)
    text = text.lower()
    text = text.strip()
    text_len = 0
    words = text.split()
    for i in words:
        i = i.strip(u'\ufeff')
        splited = i.split(u"'")
        flag = []
        for j in splited:
            if j + u"'" in wordforms or j in wordforms:
                text_len += 1
            else:
                flag.append(j)
        if flag:
            if u"'".join(flag) in wordforms:
                text_len += 1

    return text_len


def is_word(word, wordforms): #А слово ли word?...
    if word + u"'" in wordforms or word in wordforms or word.split(u"'")[0] + u"'" in wordforms:
        return True
    return False
##print france_text_len(codecs.open(u"c:\\daniil\\parallel_corpora\\fr_test1_clear.txt", "r", "utf-8").read(), read_data(wordforms_path))
##l = 0
##for i in codecs.open(u"c:\\daniil\\parallel_corpora\\fr_test1_clear.txt", "r", "utf-8"):
##    l += france_text_len(i, read_data(wordforms_path))
##print l
def create_rythm_data(text_path):
    wordforms = read_data(wordforms_path) #этакий словарь, по которому можно проверить слова с апострофом
    text_file = codecs.open(text_path, 'r', 'utf-8')
    rythm_index = read_data(rythm_path)
    index = read_data(length_path)

    for i in text_file: #Тут создается массив с индексами позиций рифм
        if u"<" not in i and u">" not in i and len(i) > 0:
            for k in i.split():
                string_len = france_text_len(k, wordforms)
                index += string_len                   
            rythm_index.append(index) #Тут он заканчивает создаваться
    write_data(rythm_path, rythm_index)
    text_file.close()
    #print index


#==============================================

def create_text_data(text_path): #Создание контекстной датабазы
    text_file = codecs.open(text_path, 'r', 'utf-8')
    text = text_file.read()
    splited_text = text.split(u"<")
    return create_stanza_data(splited_text)
    text_file.close()

def create_stanza_data(splited_text): #Индексные границы строф. Универсальная.
    strophe_index = read_data(strophes_path)
    text_data = read_data(texts_path)
    wordforms_data = read_data(wordforms_path) #этакий словарь, по которому можно проверить слова с апострофом
    verse_index = 0
    stanza_index = 0
    index = read_data(length_path)
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

            begin = index
            next_len = france_text_len(strophe_text, wordforms_data)
            end = index + next_len - 1
            index = end + 1
            strophe_index.append([verse_index, stanza_index, begin, end])

            if verse_index in text_data:
                text_data[verse_index].update({stanza_index:strophe_text})
            else:
                text_data.update({verse_index:{stanza_index:strophe_text}})
    write_data(strophes_path, strophe_index)
    write_data(texts_path, text_data)
    #print index
    return index
#create_text_data(u"c:\\daniil\\parallel\\fr_test1.txt")
#===========================================================
def create_metric_data(metric_text_path):
    metric_file = codecs.open(metric_text_path, "r", "utf-8")
    metric_info = re.compile(u'<.*?>', flags = re.U)
    local_info = re.compile(u'".*?"', flags = re.U)

    chars = read_data(gramm_path)
    wordforms = read_data(wordforms_path)
    
    index = read_data(length_path)
    for i in metric_file:
        metric_data = metric_info.findall(i)[0]
        metric_data = metric_data.strip(u"<")
        metric_data = metric_data.strip(u">")
        metric_data = local_info.findall(metric_data)
        string = metric_info.sub(u'', i)
        words_num = france_text_len(string, wordforms)
        metric_data[1] = u"metre_" + metric_data[1].strip(u'"')
        metric_data[2] = u"rhyme_" + metric_data[2].strip(u'"')
        metric_data[3] = metric_data[3].strip(u'"').replace(u" ", u"_")
        if metric_data[1] in chars:
            chars[metric_data[1]] += range(index, index + words_num)
        else:
            chars.update({metric_data[1]:range(index, index + words_num)})

        if metric_data[2] in chars:
            chars[metric_data[2]] += range(index, index + words_num)
        else:
            chars.update({metric_data[2]:range(index, index + words_num)})

        if metric_data[3] in chars:
            chars[metric_data[3]] += range(index, index + words_num)
        else:
            chars.update({metric_data[3]:range(index, index + words_num)})
            
        index += words_num
    #print index        
    write_data(gramm_path, chars)




#============================================================

def add_new_text(new_text_path, metric_path=None):
    preparced_text_path = text_preparcing(new_text_path)
    
    parced_text_path = preparced_text_path[:-14] + u"_parced.txt"
                                    
    treetagger_parcing(preparced_text_path, parced_text_path, "french")
    
    create_parcing_data(parced_text_path)
    
    create_rythm_data(new_text_path)
    
    new_index = create_text_data(new_text_path)

    if metric_path:
        create_metric_data(metric_path)
    write_data(length_path, new_index)
#===========================================================
