import csv
import numpy
import sklearn
import sklearn.ensemble
import sklearn.ensemble.forest
import multiprocessing

#is_class
def read_data(filename, classification=True):
	with open(filename, 'r', encoding='utf-8') as read_file:
		samples = []
		responses = []
		reader = csv.reader(read_file)
		column = reader.__next__()

		target_id = -1
		is_class = []
		for i in range(len(column)):
			if column[i].lower() == "target":
				target_id = i
				#is_class.append(cv2.ml.VAR_CATEGORICAL)
			elif 'has_' in column[i] or 'type_' in column[i]:
				is_class.append(True)
			else:
				is_class.append(False)
		#is_class.append(result_type)

		for line in reader:
			if len(line) != len(column):
				continue
			sample_line = []
			response_line = []
			for (x,i) in zip(line, range(len(line))):
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
	(samples,responses,is_class) = read_data("train_data.csv")
	print("Using {} CPUs".format(multiprocessing.cpu_count()))
	classifier = sklearn.ensemble.RandomForestClassifier(
		n_estimators = 1500,
		#criterion = 'entropy',
		max_features = 'auto',
		max_depth = 5,
		n_jobs = multiprocessing.cpu_count(),
		verbose = 1
	)
	classifier.fit(samples, responses)
	ret = classifier.score(samples, responses)
	print("Train score: {}".format(ret))

	(tests,responses,is_class) = read_data("test_data.csv")
	predict_result = classifier.predict_proba(tests)
	label = read_index("test_index.csv")
	print("result_len: {}, label_len: {}".format(len(predict_result), len(label)))

	print(predict_result)
	score_dict = dict()
	for (prob, key) in zip(predict_result, label):
		score_dict[key] = prob
	print(score_dict)

	submit("Test.csv", "submit.csv", score_dict)

if __name__ == '__main__':
	main()
	#main2()
