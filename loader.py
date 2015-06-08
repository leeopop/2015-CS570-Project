import csv
import os
import numpy

#return: dict, key = uniq id
#val: dict, key = column name, val = val
#example: dict: {2066053: {'affiliation': 'KAIST', 'name': 'myname'}}
def load_single_file(input_file):
	with open(input_file, 'r', encoding='utf-8') as read_file:
		reader = csv.reader(read_file)
		column = reader.__next__()
		column = [x.strip().lower() for x in column]

		id_table = dict()

		for line in reader:
			if(len(line) == 0):
				continue
			val = dict()
			key = None
			prep_key = []
			for (col, item) in zip(column, line):
				if ('id' in col) and not ('ids' in col):
					if item.isdigit():
						prep_key.append(int(item))
					else:
						prep_key.append(str(item))
					continue
				val[col] = item
			if(len(prep_key) == 1):
				key = prep_key[0]
			else:
				key = tuple(prep_key)
			id_table[key] = val
		return id_table

def load_all(directory = '.', file_list = None):
	return_data = dict()
	if file_list == None:
		file_list = ['Author', 'Conference', 'Journal', 'Paper', 'PaperAuthor', 'Test', 'Train', 'Valid', 'ValidSolution']
	for name in file_list:
		file_name = os.path.join(directory, '{}.csv'.format(name))
		return_data[name] = load_single_file(file_name)
	return return_data

def load_title_lda(total_data):
	lda_title_keyword = load_single_file('keyword_table.csv')
	word_topic_dict = dict()
	with open('lda_output.txt', 'r', encoding='utf-8') as read_file:
		for line in read_file.readlines():
			splitted = line.split()
			word = splitted[0]
			topics = splitted[1:]
			topic_sum = float(sum([int(x) for x in topics]))
			value_list = [ (float(x)/topic_sum) for x in topics]
			value_vector = numpy.array(value_list)
			word_topic_dict[int(word)] = value_vector
	total_data['title_keyword'] = lda_title_keyword
	total_data['title_keyword_topic'] = word_topic_dict


