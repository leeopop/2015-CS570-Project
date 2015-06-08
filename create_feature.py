##header begins
from collections import defaultdict
import numpy

##header ends


##from here, leeopop does
def merge_authors(total_data):
	assert('Author' in total_data.keys())
	author_data = total_data['Author']
	name_data = defaultdict(set)

	for (id, fields) in author_data.items():
		name_data[fields['name']].add(id)

	old_to_new = dict()
	new_to_old = dict()
	for (new_id, same_keys) in zip(range(len(name_data.values())), name_data.values()):
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