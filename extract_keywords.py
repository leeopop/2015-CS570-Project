import csv
import re
from loader import *
from collections import defaultdict

def split_line(single_string):
	keyword_stop = ['key', 'word']
	keyword_split = r'[\,\.\'\"\:\; \`\|\(\)]'
	splitter = re.compile(keyword_split, flags=re.UNICODE)

	single_string = single_string.lower()
	words = splitter.split(single_string)
	words = [x.strip() for x in words]
	ret = []
	for x in words:
		if len(x.strip()) == 0:
			continue
		ret.append(x)
	return ret

def create_keyword_table(paper_data, word_limit=30, skip_words = None):
	word_count = defaultdict(int)
	for (id,field) in paper_data.items():
		title = field['title']
		words = split_line(title)

		keyword_list = field['keyword']
		words += split_line(keyword_list)

		for word in words:
			if skip_words is not None:
				if word in skip_words:
					continue
			word_count[word] += 1

	keyword_table = dict()
	list_word = [x for x in word_count.items()]
	list_word = sorted(list_word, key=lambda x: x[0]) # use 1 to sort by frequency


	for (unique_id, item) in zip( range(len(list_word)), list_word):
		(word, count) = item
		if(count < word_limit):
			continue
		keyword_table[word] = unique_id
	return keyword_table


def save_keyword_table(keyword_table, output_file):
	with open(output_file, 'w', encoding='utf-8') as write_file:
		writer = csv.writer(write_file)
		writer.writerow(['id','unique'])

		for key in sorted(keyword_table.keys()):
			writer.writerow([key, keyword_table[key]])


def main():
	paper_data = load_single_file('Paper.csv')
	keyword_table = create_keyword_table(paper_data)
	save_keyword_table(keyword_table, 'keyword_table.csv')
	pass

if __name__ == '__main__':
	main()