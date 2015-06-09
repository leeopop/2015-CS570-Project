##header begins
from collections import defaultdict
from extract_keywords import split_line
import numpy
import csv

##header ends
def author_topic(total_data, num_topics=150):
	assert('Author' in total_data.keys())
	assert('PaperAuthor' in total_data.keys())
	assert('Paper' in total_data.keys())
	assert('title_keyword' in total_data.keys())

	paper = total_data['Paper']
	author = total_data['Author']
	paper_author = total_data['PaperAuthor']
	author_sum = dict()

	for (paper_id,author_id) in paper_author.keys():
		if (not paper_id in paper.keys()):
			sum_vector = numpy.zeros(num_topics)
		else:
			sum_vector = paper[paper_id]['topic_sum']
		if not (author_id in author_sum.keys()):
			author_sum[author_id] = sum_vector
		else:
			author_sum[author_id] = author_sum[author_id] + sum_vector

	for (author_id, author_field) in author.items():
		if author_id in author_sum.keys():
			vector = author_sum[author_id]
			sum = numpy.sum(vector)
			if(sum > 0.5):
				vector /= sum
			author_field['topic_sum'] = vector
		else:
			author_field['topic_sum'] = numpy.zeros(num_topics)

def paper_author_topic_sum(total_data, num_topics=150):
	assert('Author' in total_data.keys())
	assert('PaperAuthor' in total_data.keys())
	assert('Paper' in total_data.keys())
	assert('title_keyword' in total_data.keys())

	paper = total_data['Paper']
	author = total_data['Author']
	paper_author = total_data['PaperAuthor']

	for (paper_id,author_id) in paper_author.keys():
		if (paper_id in paper.keys()) and (author_id in author.keys()):
			paper_topic = paper[paper_id]['topic_sum']
			author_topic = author[author_id]['topic_sum']
			norm = numpy.linalg.norm(paper_topic)
			if norm > 0.5:
				paper_author[(paper_id, author_id)]['topic_dot'] = numpy.dot(paper_topic, author_topic)
				paper_author[(paper_id, author_id)]['has_topic_dot'] = int(1)
			else:
				paper_author[(paper_id, author_id)]['topic_dot'] = float(0)
				paper_author[(paper_id, author_id)]['has_topic_dot'] = int(0)
		else:
			paper_author[(paper_id, author_id)]['topic_dot'] = float(0)
			paper_author[(paper_id, author_id)]['has_topic_dot'] = int(0)

def save_topic_sum(total_data):
	assert('PaperAuthor' in total_data.keys())
	paper_author = total_data['PaperAuthor']
	with open('paper_author_topic_dot.csv','w',encoding='utf-8') as write_file:
		writer = csv.writer(write_file)
		writer.writerow(['paperid','authorid','topic_dot','has_topic_dot'])
		for (paper_id,author_id) in paper_author.keys():
			writer.writerow([paper_id, author_id,
			                 paper_author[(paper_id,author_id)]['topic_dot'],
			                 paper_author[(paper_id,author_id)]['has_topic_dot']])


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

def paper_topic(total_data):
	assert('title_keyword' in total_data.keys())
	assert('title_keyword_topic' in total_data.keys())
	paper = total_data['Paper']
	# key: word, value: unique id
	# e.g. title_keyword['apple']['unique'] returns unique identifier
	title_keyword = total_data['title_keyword']
	# key: word id (unique identifier), value: numpy vector
	title_keyword_topic = total_data['title_keyword_topic']
	dim = len(list(title_keyword_topic.values())[0])
	for item in paper:
		title_vector = split_line(paper[item]['title'])
		title_vector += split_line(paper[item]['keyword'])
		topic_vector = numpy.zeros(dim)
		for word in title_vector:
			if word in title_keyword:
				word_id = int(title_keyword[word]['unique'])
				word_vector = title_keyword_topic[word_id]
				topic_vector += word_vector
		sum = numpy.sum(topic_vector)
		if sum > 0.5:
			topic_vector /= sum
		paper[item]['topic_sum'] = topic_vector
	#hint: use split_line in extract_keyword.py
	#hint: merge 'title' and 'keyword' of paper data


##end


##from here, gangok does

##end