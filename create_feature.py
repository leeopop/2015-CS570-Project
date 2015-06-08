##header begins
from collections import defaultdict
import numpy
import csv

##header ends
def author_title(total_data, num_topics=150):
	assert('Author' in total_data.keys())
	assert('PaperAuthor' in total_data.keys())
	assert('Paper' in total_data.keys())
	assert('title_keyword' in total_data.keys())

	paper = total_data['Paper']
	author = total_data['Author']
	paper_author = total_data['PaperAuthor']
	author_sum = dict()

	for (paper_id,author_id) in paper_author.keys():
		sum_vector = paper[paper_id]['topic_sum']
		if not (author_id in author_sum.keys()):
			author_sum[author_id] = sum_vector
		else:
			author_sum[author_id] = numpy.sum([author_sum[author_id], sum_vector])

	for (author_id, author_field) in author:
		if author_id in author_sum.keys():
			author_field['topic_sum'] = author_sum[author_id]
		else:
			author_field['topic_sum'] = numpy.zeros(num_topics)

def paper_author_topic_sum(total_data):
	assert('Author' in total_data.keys())
	assert('PaperAuthor' in total_data.keys())
	assert('Paper' in total_data.keys())
	assert('title_keyword' in total_data.keys())

	paper = total_data['Paper']
	author = total_data['Author']
	paper_author = total_data['PaperAuthor']
	author_sum = dict()

	for (paper_id,author_id) in paper_author.keys():
		paper_topic = paper[paper_id]['topic_sum']
		author_topic = author[author_id]['topic_sum']
		paper_author[(paper_id, author_id)]['topic_dot'] = numpy.dot(paper_topic, author_topic)

def save_topic_sum(total_data):
	assert('PaperAuthor' in total_data.keys())
	paper_author = total_data['PaperAuthor']
	with open('paper_author_topic_dot.csv','w',encoding='utf-8') as write_file:
		writer = csv.writer(write_file)
		writer.writerow(['paperid','authorid','topic_dot'])
		for (paper_id,author_id) in paper_author.keys():
			writer.writerow([paper_id, author_id,paper_author[(paper_id,author_id)]['topic_dot']])


##from here, leeopop does
def merge_authors(total_data):
	assert('Author' in total_data.keys())
	author_data = total_data['Author']
	name_data = defaultdict(set)

	for (id, fields) in author_data.items():
		name_data[fields['name']].add(id)

	old_to_new = dict()
	new_to_old = dict()
	for (new_id, same_keys) in zip(range(len(name_data)), name_data.values()):
		for old in same_keys:
			old_to_new[old] = new_id
		new_to_old[new_id] = same_keys

	total_data['old_to_new'] = old_to_new
	total_data['new_to_old'] = new_to_old

def convert_title(total_data):
	assert('title_keyword' in total_data.keys())
	assert('title_keyword_topic' in total_data.keys())

	# key: word, value: unique id
	# e.g. title_keyword['apple']['unique'] returns unique identifier
	title_keyword = total_data['title_keyword']

	# key: word id (unique identifier), value: numpy vector
	title_keyword_topic = total_data['title_keyword_topic']

	#hint: use split_line in extract_keyword.py
	#hint: merge 'title' and 'keyword' of paper data


##end


##from here, gangok does

##end