import csv
import numpy
import sklearn
import sklearn.ensemble
import sklearn.ensemble.forest
import multiprocessing
from loader import load_single_file

#is_class
def read_data(filename, classification=True, limit_index=None):
	with open(filename, 'r', encoding='utf-8') as read_file:
		samples = []
		responses = []
		reader = csv.reader(read_file)
		column = reader.__next__()

		target_id = -1
		is_class = []
		available = set()
		for i in range(len(column)):
			if limit_index is not None:
				if not column[i].lower() in limit_index:
					continue
			if column[i].lower() == "target":
				target_id = i
				#is_class.append(cv2.ml.VAR_CATEGORICAL)
			elif 'has_' in column[i] or 'type_' in column[i]:
				is_class.append(True)
			else:
				is_class.append(False)
			available.add(i)
		#is_class.append(result_type)

		for line in reader:
			if len(line) != len(column):
				continue
			sample_line = []
			response_line = []
			for (x,i) in zip(line, range(len(line))):
				if i not in available:
					continue
				if i == target_id:
					if x.isdigit():
						response_line.append(int(x))
					else:
						response_line.append(int(-1))
					continue
				sample_line.append(x)
			samples.append(sample_line)
			responses.append(response_line)
		result_dtype = numpy.float32
		if(classification == True):
			result_dtype = numpy.int32
		return (numpy.array(samples, dtype=numpy.float32),
		        numpy.array(responses, dtype=result_dtype),
		        numpy.array(is_class, dtype=numpy.int32))

def read_index(filename):
	mapping = []
	with open(filename, 'r', encoding='utf-8') as read_file:
		reader = csv.reader(read_file)
		column = reader.__next__()
		author_id = -1
		paper_id = -1

		for i in range(len(column)):
			if column[i].lower().strip() == "authorid":
				author_id = i
				#is_class.append(cv2.ml.VAR_CATEGORICAL)
			elif column[i].lower().strip() == "paperid":
				paper_id = i

		for line in reader:
			if len(line) != len(column):
				continue
			author = None
			paper = None
			for (x,i) in zip(line, range(len(line))):
				if i == author_id:
					author = int(x)
				elif i == paper_id:
					paper = int(x)
			mapping.append((author,paper))
	return mapping

def submit(input_file, output_file, score_dict):
	with open(input_file, "r", encoding='utf-8') as read_file:
		with open(output_file, "w", encoding='utf-8') as write_file:
			reader = csv.reader(read_file)
			column = reader.__next__()
			assert(len(column) == 2)

			writer = csv.writer(write_file)
			writer.writerow(column)

			for [author,papers] in reader:
				list_papers = papers.strip().split()
				list_papers = sorted(list_papers, key=lambda paper: score_dict[(int(author), int(paper))][0])
				writer.writerow([author, ' '.join(list_papers)])



def main():
	limit_index=['target','topic_dot','has_topic_dot']
	#limit_index=None
	(samples,responses,is_class) = read_data("train_data_dot.csv", limit_index=limit_index)
	print("Using {} CPUs".format(multiprocessing.cpu_count()))

	#This parameter works for development environment
	classifier = sklearn.ensemble.RandomForestClassifier(
		n_estimators = 1500,
		criterion = 'entropy',
		max_features = None,
		class_weight='auto',
		n_jobs = multiprocessing.cpu_count(),
		verbose = 1
	)
	classifier.fit(samples, responses)
	ret = classifier.score(samples, responses)
	print("Train score: {}".format(ret))

	(tests,responses,is_class) = read_data("test_data_dot.csv", limit_index=limit_index)
	predict_result = classifier.predict_proba(tests)
	label = read_index("test_index.csv")
	print("result_len: {}, label_len: {}".format(len(predict_result), len(label)))

	score_dict = dict()
	for (prob, key) in zip(predict_result, label):
		score_dict[key] = prob

	submit("Test.csv", "submit.csv", score_dict)

def add_column(orig,orig_index,new,new_file, new_column):
	label = read_index(orig_index)

	with open(orig, 'r', encoding='utf-8') as read_file:
		reader = csv.reader(read_file)
		column = reader.__next__()

		new_data = load_single_file(new) #paper,author
		with open(new_file, 'w', encoding='utf-8') as write_file:
			writer = csv.writer(write_file)

			column += new_column
			writer.writerow(column)

			for (line,(author_id, paper_id)) in zip(reader, label):
				for new_col in new_column:
					line.append(new_data[(paper_id,author_id)][new_col])
				writer.writerow(line)
	pass

if __name__ == '__main__':
	main()
	#add_column('test_data.csv','test_index.csv','paper_author_topic_dot.csv','test_data_dot.csv',['topic_dot','has_topic_dot'])
	#add_column('train_data.csv','train_index.csv','paper_author_topic_dot.csv','train_data_dot.csv',['topic_dot','has_topic_dot'])
