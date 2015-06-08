from loader import *
from extract_keywords import split_line
from collections import defaultdict

def main():
	keyword_data = load_single_file('keyword_table.csv')
	paper_data = load_single_file('Paper.csv')

	with open('lda_input.txt', 'w', encoding='utf-8') as write_file:
		for paper_id in paper_data.keys():
			paper = paper_data[paper_id]
			title = paper['title']
			keyword = paper['keyword']

			word_list = split_line(title)
			word_list += split_line(keyword)

			counter = defaultdict(int)
			for word in word_list:
				if word in keyword_data.keys():
					unique_id = keyword_data[word]['unique']
					counter[unique_id] += 1

			line = ''
			for key in sorted(counter.keys()):
				count = counter[key]
				line += '{} {} '.format(key, count)
			line = line.strip()
			if len(line) == 0:
				continue
			line += '\n'

			write_file.write(line)
	pass

if __name__ == '__main__':
	main()