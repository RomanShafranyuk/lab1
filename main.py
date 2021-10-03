from math import *
# Задание №1
import zipfile
import os
import hashlib
import re
import requests
import csv
# os.mkdir('D:\\new_dir')
directory_to_extract_to = "D:\\new_dir"  # директория извлечения файлов архива
# arch_file = zipfile.ZipFile('D:\\lab1\\tiff-4.2.0_lab1.zip')  # путь к архиву
# arch_file.extractall(directory_to_extract_to)
# arch_file.close()
txt_files = []
for i, j, k in os.walk(directory_to_extract_to):
    for t in k:
        if ".txt" in t:
            txt_files.append(i + '\\' + t)
# print(txt_files)
result = []
directories = []
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файла
for i in txt_files:
    file_data = open(i, "rb")
    content = file_data.read()
    result.append(hashlib.md5(content).hexdigest())
    file_data.close()
# print(result)
for i, j, k in os.walk(directory_to_extract_to):
    for t in k:
        file_data = open(i + '\\' + t, "rb")
        content = file_data.read()
        if hashlib.md5(content).hexdigest() == target_hash:
            target_file = i
            target_file_data = content
print(target_file)
print(target_file_data)
# задача 4

r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы
counter = 0
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
# print(lines)
regex = "\(.*?\)"
headers = []
for line in lines:
    if counter == 0:
        headers = re.sub('<.*?>', ' ', line)
        #print(headers)
        headers = re.findall(r'Заболели|Умерли|Вылечились|Активные случаи', headers)
        #print(headers)
    else:
        temp = re.sub('<.*?>', ';', line)
        temp = re.sub(regex, '', temp)
        temp = re.sub(';+', ';', temp)
        temp = temp[1: len(temp)-1]
        temp = re.sub('\s(?=\d)', '', temp)
        temp = re.sub('(?<=\d)\s', '', temp)
        temp = re.sub('(?<=0)\*', '',temp)
        temp = re.sub('_', '-1', temp)
        #print(temp)
        tmp_split = temp.split(';')
        if len(tmp_split) == 6:
            tmp_split.pop(0)
        #print(tmp_split)
        country_name = tmp_split[0]
        country_name = re.sub('.*\s\s', '', country_name)
        #print(country_name)
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)
    counter += 1
headers.insert(0, ' ')
print(headers)
print(result_dct)
# Задание №5
# Запись данных из полученного словаря в файл
output = open('data.csv', 'w')
w = csv.writer(output, delimiter=";")
w.writerow(headers)
for key in result_dct.keys():
    w.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
output.close()

#target_country = input("Введите название страны: ")
#print(result_dct[target_country])