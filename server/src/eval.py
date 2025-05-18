"""Function for data conversion
"""
import unittest
import re
import csv
import pandas as pd
from collections import defaultdict, OrderedDict
from nltk.tokenize import WordPunctTokenizer
from sklearn.metrics import classification_report

class Token(object):

    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

    def __repr__(self):
        return str( (self.text, self.start, self.end) )


def remove_xml_tags(entity):
    entity = re.sub(r"<ENAMEX TYPE=\"(.+?)\">", "", entity)
    entity = re.sub(r"</ENAMEX>", "", entity)
    return entity


def tokenize(text):
    tokens = []
    # tokenizer = TreebankWordTokenizer()
    tokenizer = WordPunctTokenizer()

    syllables = tokenizer.tokenize(text)
    syllables = [ '"' if s == "``" or s == "''" else s for s in syllables ]

    _pos = 0
    for s in syllables:
        start = text.find(s, _pos)
        end = start + len(s)
        _pos = end
        syl = Token(s, start, end)
        tokens.append(syl)
    return tokens


def depth_level(astring):
    """
    E.g.,
    Tôi là sinh viên -> 0
    ĐHQG <ENAMEX>Hà Nội</ENAMEX> -> 1
    Khoa thanh nhạc <ENAMEX>Học viên âm nhạc <ENAMEX>HCM</ENAMEX></ENAMEX> -> 2
    Args:
        astring: input string with XML tags
    Returns:
        The depth level of a string
    """
    level = 0
    first = True
    first_add_child = True
    OPEN_TAG = 1
    stack = []
    i = 0
    while i < len(astring):
        # print(astring[i:], stack, level)
        if astring[i:].startswith("<ENAMEX TYPE="):
            if first:
                level += 1
                first = False
            if len(stack) > 0:
                if first_add_child:
                    level += 1
                    first_add_child = False
            stack.append(OPEN_TAG)
            i += len("<ENAMEX TYPE=")
        elif astring[i:].startswith("</ENAMEX>"):
            stack.pop()
            i += len("</ENAMEX>")
        else:
            i += 1
    return level


def get_entities(line):
    """

    Args:
        line (string): Input sentence (single sentence) with XML tags
        E.g., Đây là lý do khiến <ENAMEX TYPE=\"PERSON\">Yoon Ah</ENAMEX> quyết định cắt mái tóc dài 'nữ thần'

    Returns:
        raw (string): raw sentence
        entities (list): list of entities (json object) (Wit.ai)
    """
    debug = False
    raw = ""
    entities = []

   #  regex_opentag = re.compile(r"<ENAMEX TYPE=\"(.+?)\">")
    regex_opentag = re.compile(r'<ENAMEX TYPE="(.+?)">')
    regex_closetag = re.compile(r"</ENAMEX>")
    next_start_pos = 0
    match1 = regex_opentag.search(line, next_start_pos)
    stack = []
    if match1:
        raw += line[0:match1.start()]
        next_start_pos = match1.end()
        stack.append(match1)
    else:
        raw = line

    while len(stack) != 0:
        if debug: print("#Current stack", stack)
        match1 = stack.pop()
        if debug: print("#From next_start_pos {}: {}".format(next_start_pos, line[next_start_pos:]))
        next_closetag1 = regex_closetag.search(line, next_start_pos)
        if not next_closetag1:
            print(line)
            raise ValueError("Close tag not found")
        next_end_pos1 = next_closetag1.start()
        match2 = regex_opentag.search(line, next_start_pos, next_end_pos1)
        if match2:
            raw += line[next_start_pos:match2.start()]
            next_start_pos1 = match2.end()
            next_closetag2 = regex_closetag.search(line, next_start_pos1)
            if not next_closetag2:
                raise ValueError("Close tag not found")
            next_end_pos2 = next_closetag2.start()
            match3 = regex_opentag.search(line, next_start_pos1, next_end_pos2)
            if match3:
                level = 1
                raw += line[next_start_pos1:match3.start()]
                next_start_pos2 = match3.end()
                value = line[next_start_pos2:next_end_pos2]
                _type = match3.group(1)

                entity = OrderedDict()
                entity["type"] = _type
                entity["value"] = value
                entity["start"] = len(raw)
                entity["end"] = entity["start"] + len(value)
                entity["level"] = level
                entities.append(entity)

                if debug: print("#Entity:", value, _type, level)
                raw += value
                next_start_pos = next_closetag2.end()
                stack.append(match1)
                stack.append(match2)
            else:
                # Get entity between match2 and next_closetag2
                value = remove_xml_tags( line[match2.end():next_end_pos2] )
                _type = match2.group(1)
                # abc <ENAMEX> xyz <ENAMEX>dhg</ENAMEX> mpq</ENAMEX> r
                level = 1 + depth_level( line[match2.end():next_end_pos2] )
                if debug: print("#current: ", raw)
                raw += line[next_start_pos1:next_closetag2.start()]
                if debug: print("->", raw)
                entity = OrderedDict()
                entity["type"] = _type
                entity["value"] = value
                entity["start"] = len(raw) - len(value)
                entity["end"] = len(raw)
                entity["level"] = level
                entities.append(entity)

                if debug: print("#Entity:", value, _type, level)
                next_start_pos = next_closetag2.end()
                stack.append(match1)
                next_match2 = regex_opentag.search(line, next_start_pos)
                next_closetag3 = regex_closetag.search(line, next_start_pos)

                if next_match2:
                    if next_closetag3 and next_match2.start() < next_closetag3.start():
                        if debug: print("Next match2:", line[next_match2.start():])
                        if debug: print("#current: ", raw)
                        raw += line[next_start_pos:next_match2.start()]
                        if debug: print("->", raw)
                        next_start_pos = next_match2.end()
                        stack.append(next_match2)
        else:
            # Get entity between match1 and next_closetag1
            value = remove_xml_tags( line[match1.end():next_closetag1.start()] )
            _type = match1.group(1)
            level = 1 + depth_level( line[match1.end():next_closetag1.start()] )
            if debug: print("#current: ", raw)
            raw += line[next_start_pos:next_closetag1.start()]
            if debug: print("->", raw)
            entity = OrderedDict()
            entity["type"] = _type
            entity["value"] = value
            entity["start"] = len(raw) - len(value)
            entity["end"] = len(raw)
            entity["level"] = level
            entities.append(entity)
            if debug: print("#Entity:", value, _type, level)
            next_start_pos = next_closetag1.end()

            next_match1 = regex_opentag.search(line, next_start_pos)
            next_closetag3 = regex_closetag.search(line, next_start_pos)
            if next_match1:
                if next_closetag3 and next_match1.start() < next_closetag3.start():
                    if debug: print("#Next match1:", line[next_match1.start():])
                    if debug: print("#current: ", raw)
                    raw += line[next_start_pos:next_match1.start()]
                    if debug: print("->", raw)
                    next_start_pos = next_match1.end()
                    stack.append(next_match1)
                else:
                    continue
            else:
                if debug: print("#current: ", raw)
                if debug: print("{} {}".format(next_closetag1.end(), line[next_closetag1.end():]))
                if not re.search(r"</ENAMEX>", line[next_closetag1.end():]):
                    raw += line[next_closetag1.end():]
                    if debug: print("->", raw)

    return raw, entities

def get_entities_v2(line):
    """

    Args:
        line (string): Input sentence (single sentence) with XML tags
        E.g., Đây là lý do khiến <ENAMEX TYPE=\"PERSON\">Yoon Ah</ENAMEX> quyết định cắt mái tóc dài 'nữ thần'

    Returns:
        raw (string): raw sentence
        entities (list): list of entities (json object) (Wit.ai)
    """
    debug = False
    raw = ""
    entities1 = []
    entities2 = []
    entities3 = []

   #  regex_opentag = re.compile(r"<ENAMEX TYPE=\"(.+?)\">")
    regex_opentag = re.compile(r'<ENAMEX TYPE="(.+?)">')
    regex_closetag = re.compile(r"</ENAMEX>")
    next_start_pos = 0
    match1 = regex_opentag.search(line, next_start_pos)
    stack = []
    if match1:
        raw += line[0:match1.start()]
        next_start_pos = match1.end()
        stack.append(match1)
    else:
        raw = line

    while len(stack) != 0:
        if debug: print("#Current stack", stack)
        match1 = stack.pop()
        if debug: print("#From next_start_pos {}: {}".format(next_start_pos, line[next_start_pos:]))
        next_closetag1 = regex_closetag.search(line, next_start_pos)
        if not next_closetag1:
            print(line)
            raise ValueError("Close tag not found")
        next_end_pos1 = next_closetag1.start()
        match2 = regex_opentag.search(line, next_start_pos, next_end_pos1)
        if match2:
            raw += line[next_start_pos:match2.start()]
            next_start_pos1 = match2.end()
            next_closetag2 = regex_closetag.search(line, next_start_pos1)
            if not next_closetag2:
                raise ValueError("Close tag not found")
            next_end_pos2 = next_closetag2.start()
            match3 = regex_opentag.search(line, next_start_pos1, next_end_pos2)
            if match3:
                level = 1
                raw += line[next_start_pos1:match3.start()]
                next_start_pos2 = match3.end()
                value = line[next_start_pos2:next_end_pos2]
                _type = match3.group(1)

                entity = OrderedDict()
                entity["type"] = _type
                entity["value"] = value
                if level == 1:
                  entities1.append(entity)
                elif level == 2:
                  entities2.append(entity)
                else:
                  entities3.append(entity)

                if debug: print("#Entity:", value, _type, level)
                raw += value
                next_start_pos = next_closetag2.end()
                stack.append(match1)
                stack.append(match2)
            else:
                # Get entity between match2 and next_closetag2
                value = remove_xml_tags( line[match2.end():next_end_pos2] )
                _type = match2.group(1)
                # abc <ENAMEX> xyz <ENAMEX>dhg</ENAMEX> mpq</ENAMEX> r
                level = 1 + depth_level( line[match2.end():next_end_pos2] )
                if debug: print("#current: ", raw)
                raw += line[next_start_pos1:next_closetag2.start()]
                if debug: print("->", raw)
                entity = OrderedDict()
                entity["type"] = _type
                entity["value"] = value
                if level == 1:
                    entities1.append(entity)
                elif level == 2:
                    entities2.append(entity)
                else:
                    entities3.append(entity)
               

                if debug: print("#Entity:", value, _type, level)
                next_start_pos = next_closetag2.end()
                stack.append(match1)
                next_match2 = regex_opentag.search(line, next_start_pos)
                next_closetag3 = regex_closetag.search(line, next_start_pos)

                if next_match2:
                    if next_closetag3 and next_match2.start() < next_closetag3.start():
                        if debug: print("Next match2:", line[next_match2.start():])
                        if debug: print("#current: ", raw)
                        raw += line[next_start_pos:next_match2.start()]
                        if debug: print("->", raw)
                        next_start_pos = next_match2.end()
                        stack.append(next_match2)
        else:
            # Get entity between match1 and next_closetag1
            value = remove_xml_tags( line[match1.end():next_closetag1.start()] )
            _type = match1.group(1)
            level = 1 + depth_level( line[match1.end():next_closetag1.start()] )
            if debug: print("#current: ", raw)
            raw += line[next_start_pos:next_closetag1.start()]
            if debug: print("->", raw)
            entity = OrderedDict()
            entity["type"] = _type
            entity["value"] = value
            if level == 1:
               entities1.append(entity)
            elif level == 2:
               entities2.append(entity)
            else:
               entities3.append(entity)
            if debug: print("#Entity:", value, _type, level)
            next_start_pos = next_closetag1.end()

            next_match1 = regex_opentag.search(line, next_start_pos)
            next_closetag3 = regex_closetag.search(line, next_start_pos)
            if next_match1:
                if next_closetag3 and next_match1.start() < next_closetag3.start():
                    if debug: print("#Next match1:", line[next_match1.start():])
                    if debug: print("#current: ", raw)
                    raw += line[next_start_pos:next_match1.start()]
                    if debug: print("->", raw)
                    next_start_pos = next_match1.end()
                    stack.append(next_match1)
                else:
                    continue
            else:
                if debug: print("#current: ", raw)
                if debug: print("{} {}".format(next_closetag1.end(), line[next_closetag1.end():]))
                if not re.search(r"</ENAMEX>", line[next_closetag1.end():]):
                    raw += line[next_closetag1.end():]
                    if debug: print("->", raw)

    return entities1, entities2, entities3


def find_syl_index(start, end, syllables):
    """Find start and end indexes of syllables
    """
    start_syl_id = None
    end_syl_id   = None
    for i, syl in enumerate(syllables):
        if syl.start == start:
            start_syl_id = i
        if syl.end == end:
            end_syl_id = i+1

        if i > 0 and syl.start >= start and syllables[i-1].end <= start:
            start_syl_id = i
        if i == 0 and syl.start > start:
            start_syl_id = i

        if i < len(syllables)-1 and syl.end < end and syllables[i+1].start > end:
            end_syl_id = i+1

        if syl.end >= end and syl.start < end:
            end_syl_id = i+1
        if i == len(syllables)-1 and syl.end <= end:
            end_syl_id = i+1

        if i > 0 and syl.start < start and syllables[i-1].end < start: 
            start_syl_id = i

        if syl.start < start and syl.end >= end:
            start_syl_id = i
            end_syl_id = i + 1

        if i == 0 and len(syllables) > 0 and syl.start < start and syl.end < end:
            start_syl_id = i

   #  if start_syl_id == None:
   #      print("Cannot find start_syl_id '{}' (end={}) in '{}'".format(start, end, syllables))
   #  if end_syl_id == None:
   #      print("Cannot find end_syl_id '{}' (start={}) in '{}'".format(end, start, syllables))

    return start_syl_id, end_syl_id

count = 0

def xml2tokens(xml_tagged_sent):
    global count
    """Convert XML-based tagged sentence into CoNLL format based on syllables
    Args:
        xml_tagged_sent (string): Input sentence (single sentence) with XML tags

    Returns:
        tokens (list): list of tuples (tk, level1_tag, level2_tag)
          level1_tag is entity tag (BIO scheme) at the level 1
          level2_tag is entity tag at the level 2 (nested entity)
    """
    raw, entities = get_entities(xml_tagged_sent)
    if re.search(r"ENAMEX", raw):
      #   print("Search", raw)
        count += 1

    tokens = tokenize(raw)
    level1_syl_tags = ["O" for i in range(len(tokens))]
    level2_syl_tags = ["O" for i in range(len(tokens))]
    level3_syl_tags = ["O" for i in range(len(tokens))]
    flag = False
    for entity in entities:
        value = entity["value"]
        start = entity["start"]
        end = entity["end"]
        entity_type = entity["type"]
        start_syl_id, end_syl_id = find_syl_index(start, end, tokens)
        if start_syl_id != None and end_syl_id != None:
            if entity["level"] == 1:
                level1_syl_tags[start_syl_id] = "B-" + entity_type
                for i in range(start_syl_id + 1, end_syl_id):
                    level1_syl_tags[i] = "I-" + entity_type
            elif entity["level"] == 2:
                level2_syl_tags[start_syl_id] = "B-" + entity_type
                for i in range(start_syl_id + 1, end_syl_id):
                    level2_syl_tags[i] = "I-" + entity_type
            else:
                level3_syl_tags[start_syl_id] = "B-" + entity_type
                for i in range(start_syl_id + 1, end_syl_id):
                    level3_syl_tags[i] = "I-" + entity_type
        else:
            # print("{},{},\"{}\" in '{}' ({})".format(start,end,value,raw,xml_tagged_sent))
            flag = True
    res = list(zip([ tk.text for tk in tokens], level1_syl_tags, level2_syl_tags, level3_syl_tags))
    return res, flag


def calculate_token(goal_data, manual_data):
    tokens_goal, flag_goal = xml2tokens(goal_data)
    tokens_manual, flag_manual = xml2tokens(manual_data)
    len_tokens_goal = len(tokens_goal)
    len_tokens_manual = len(tokens_manual)
    y_goal = []
    y_manual = []

    for token_goal, token_manual in zip(tokens_goal, tokens_manual):
        goal_label1 = token_goal[1]
        goal_label2 = token_goal[2]
        goal_label3 = token_goal[3]

        manual_label1 = token_manual[1]
        manual_label2 = token_manual[2]
        manual_label3 = token_manual[3]

        # Nối 3 cấp lại để tạo thành 1 nhãn duy nhất
        y_goal.append(goal_label1 + " - " + goal_label2 + " - " + goal_label3)
        y_manual.append(manual_label1 + " - " + manual_label2 + " - " + manual_label3)

    return  len_tokens_goal, len_tokens_manual, y_goal, y_manual
 

def load_data_to_caculate_accuracy(goal_path, manual_path, frag):
    df_goal = pd.read_csv(goal_path, encoding="utf-8", quoting=csv.QUOTE_ALL)
    df_manual = pd.read_csv(manual_path, encoding="utf-8", quoting=csv.QUOTE_ALL)
    if frag == True:
      list_goal = df_goal['sentences'].to_list()
      list_manual = df_manual['tagged_sents'].to_list()
    else:
      list_goal = df_goal['tagged_sents'].to_list()
      list_manual = df_manual['tagged_sents'].to_list() 

    all_y_goal = []
    all_y_manual = []

    for goal, manual in zip(list_goal, list_manual):
        result = calculate_token(goal, manual)
        if result[0] != result[1]:
         continue
         
        y_goal = result[2]
        y_manual = result[3] 
        
        all_y_goal.extend(y_goal)
        all_y_manual.extend(y_manual)

    print(classification_report(all_y_goal, all_y_manual, zero_division=0))


a = []
b = []

def merge_by_value_unique(tuple1: tuple, tuple2: tuple):
    combined = []
    for part in tuple1 + tuple2:
        combined.extend(part)

    value_dict = {}
    for item in combined:
        value = item['value']
        value_dict[value] = item

    merged = list(value_dict.values())

    # Xóa key 'level' trong mỗi OrderedDict
    for item in merged:
        item.pop('level', None)  # dùng pop cho an toàn, nếu không có 'level' thì cũng không lỗi

    return merged

def caculate_f1(goal_data: str, manual_data: str):
    global a, b
    y_goal, y_manual = [], []
    result_goal = get_entities_v2(goal_data)  # list of list per sentence
    result_manual = get_entities_v2(manual_data)
    all_ner = merge_by_value_unique(result_goal, result_manual)
    goal_ner  = [item for sublist in result_goal for item in sublist]
    manual_ner = [item for sublist in result_manual for item in sublist]
    for ner in all_ner:
      ner_value = ner['value']
      # Tìm xem goal và manual có tồn tại 'value' này không
      goal_match = next((item for item in goal_ner if item['value'] == ner_value), None)
      manual_match = next((item for item in manual_ner if item['value'] == ner_value), None)

      if goal_match and manual_match:
            y_goal.append(goal_match['type'])
            y_manual.append(manual_match['type'])
      elif goal_match and not manual_match:
         y_goal.append(goal_match['type'])
         y_manual.append('O')
      elif manual_match and not goal_match:
         y_goal.append('O')
         y_manual.append(manual_match['type'])
      # else: không có trường hợp nào cần skip cả

    if len(y_goal) != len(y_manual):
        print("Lỗi: Kích thước y_goal và y_manual không khớp!")
   #  print(y_goal, y_manual)
    return y_goal, y_manual


def load_data_to_caculate_f1(goal_path, manual_path, frag):
    
    df_goal = pd.read_csv(goal_path, encoding="utf-8", quoting=csv.QUOTE_ALL)
    df_manual = pd.read_csv(manual_path, encoding="utf-8", quoting=csv.QUOTE_ALL)
    if frag == True:
      list_goal = df_goal['sentences'].to_list()
      list_manual = df_manual['tagged_sents'].to_list()
    else:
      list_goal = df_goal['tagged_sents'].to_list()
      list_manual = df_manual['tagged_sents'].to_list() 

    all_y_goal = []
    all_y_manual = []

    for goal, manual in zip(list_goal, list_manual):
        result = caculate_f1(goal, manual)
        
        all_y_goal.extend(result[0])
        all_y_manual.extend(result[1])

    print(classification_report(all_y_goal, all_y_manual, zero_division=0))


if __name__ == "__main__":
   # #Set1
   # goal_path = r"D:\HK6\CS321_NNHNL\evaluate\set1\goal_set1.csv"
   # manual_path_1 = r"D:\HK6\CS321_NNHNL\evaluate\set1\anh_set01.csv"
   # manual_path_2 = r"D:\HK6\CS321_NNHNL\evaluate\set1\duyen_set1.csv"
   # manual_path_3 = r"D:\HK6\CS321_NNHNL\evaluate\set1\khanh_set1.csv"

   # # Set2
   # goal_path = r"D:\HK6\CS321_NNHNL\evaluate\set2\goal_set2.csv"
   # manual_path_1 = r"D:\HK6\CS321_NNHNL\evaluate\set2\anh_set02.csv"
   # manual_path_2 = r"D:\HK6\CS321_NNHNL\evaluate\set2\duyen_set2.csv"
   # manual_path_3 = r"D:\HK6\CS321_NNHNL\evaluate\set2\khanh_set2.csv"

   # #Set3
   # goal_path = r"D:\HK6\CS321_NNHNL\evaluate\set3\goal_set3.csv"
   # manual_path_1 = r"D:\HK6\CS321_NNHNL\evaluate\set3\anh_set03.csv"
   # manual_path_2 = r"D:\HK6\CS321_NNHNL\evaluate\set3\duyen_set3.csv"
   # manual_path_3 = r"D:\HK6\CS321_NNHNL\evaluate\set3\khanh_set3.csv"

   # #Set4
   # goal_path = r"D:\HK6\CS321_NNHNL\evaluate\set4\goal_set4.csv"
   # manual_path_1 = r"D:\HK6\CS321_NNHNL\evaluate\set4\annotation_anh_set4.csv"
   # manual_path_2 = r"D:\HK6\CS321_NNHNL\evaluate\set4\annotation_duyen_set4.csv"
   # manual_path_3 = r"D:\HK6\CS321_NNHNL\evaluate\set4\annotation_khanh_set4.csv"

   # #Set5
   # goal_path = r"D:\HK6\CS321_NNHNL\evaluate\set5\goal_set5.csv"
   # manual_path_1 = r"D:\HK6\CS321_NNHNL\evaluate\set5\annotation_anh_set5.csv"
   # manual_path_2 = r"D:\HK6\CS321_NNHNL\evaluate\set5\annotation_duyen_set5.csv"
   # manual_path_3 = r"D:\HK6\CS321_NNHNL\evaluate\set5\annotation_khanh_set5.csv"

   # #Set6
   # goal_path = r"D:\HK6\CS321_NNHNL\evaluate\set6\goal_set6.csv"
   # manual_path_1 = r"D:\HK6\CS321_NNHNL\evaluate\set6\annotation_anh_set6.csv"
   # manual_path_2 = r"D:\HK6\CS321_NNHNL\evaluate\set6\annotation_duyen_set6.csv"
   # manual_path_3 = r"D:\HK6\CS321_NNHNL\evaluate\set6\annotation_khanh_set6.csv"

   #Set7
   goal_path = r"D:\HK6\CS321_NNHNL\evaluate\set7\goal_set7.csv"
   manual_path_1 = r"D:\HK6\CS321_NNHNL\evaluate\set7\annotation_anh_set7.csv"
   manual_path_2 = r"D:\HK6\CS321_NNHNL\evaluate\set7\annotation_duyen_set7.csv"
   manual_path_3 = r"D:\HK6\CS321_NNHNL\evaluate\set7\annotation_khanh_set7.csv"

   load_data_to_caculate_f1(goal_path, manual_path_3, True)
   # load_data_to_caculate_f1(manual_path_1, manual_path_2, False)

   
