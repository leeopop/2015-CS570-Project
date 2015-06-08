import csv
import os

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
				if('id' in col):
					prep_key.append(int(item))
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
		file_list = ['Author', 'Conference', 'Journal', 'PaperAuthor', 'Test', 'Train', 'Valid', 'ValidSolution']
	for name in file_list:
		file_name = os.path.join(directory, '{}.csv'.format(name))
		return_data[name] = load_single_file(file_name)
	return return_data


load_all()