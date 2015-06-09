import csv
import numpy
import sklearn
import sklearn.base
import sklearn.naive_bayes
import sklearn.ensemble
import sklearn.ensemble.forest
import sklearn.linear_model
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
	limit_index=None
	limit_index=['target']
	orig_index = ['year','count_authorid','count_paperid','count_authorid_paperid','count_authorid_paperid_onameid',
	              'count_paperid_onameid', 'count_upper_authorid_paperid','count_upper_paperid','count_unq_authorid',
	              'count_unq_paperid','count_unq_paperid_onameid','count_author_paperid','count_unq_author_paperid',
	              'count_same_aff_paperid','count_aff_authorid_paperid','count_aff_paperid','count_datadup_authorid_paperid',
	              'has_conferenceid','has_journalid','has_year','has_title','has_keyword','count_not_abb_paperid']
	lda_index = ['topic_dot','has_topic_dot']
	lda_cross_index = ['topic_cross_0',
	            'topic_cross_1', 'topic_cross_2', 'topic_cross_3', 'topic_cross_4', 'topic_cross_5',
	            'topic_cross_6', 'topic_cross_7', 'topic_cross_8', 'topic_cross_9', 'topic_cross_10',
	            'topic_cross_11', 'topic_cross_12', 'topic_cross_13', 'topic_cross_14', 'topic_cross_15',
	            'topic_cross_16', 'topic_cross_17', 'topic_cross_18', 'topic_cross_19', 'topic_cross_20',
	            'topic_cross_21', 'topic_cross_22', 'topic_cross_23', 'topic_cross_24', 'topic_cross_25',
	            'topic_cross_26', 'topic_cross_27', 'topic_cross_28', 'topic_cross_29', 'topic_cross_30',
	            'topic_cross_31', 'topic_cross_32', 'topic_cross_33', 'topic_cross_34', 'topic_cross_35',
	            'topic_cross_36', 'topic_cross_37', 'topic_cross_38', 'topic_cross_39', 'topic_cross_40',
	            'topic_cross_41', 'topic_cross_42', 'topic_cross_43', 'topic_cross_44', 'topic_cross_45',
	            'topic_cross_46', 'topic_cross_47', 'topic_cross_48', 'topic_cross_49', 'topic_cross_50',
	            'topic_cross_51', 'topic_cross_52', 'topic_cross_53', 'topic_cross_54', 'topic_cross_55',
	            'topic_cross_56', 'topic_cross_57', 'topic_cross_58', 'topic_cross_59', 'topic_cross_60',
	            'topic_cross_61', 'topic_cross_62', 'topic_cross_63', 'topic_cross_64', 'topic_cross_65',
	            'topic_cross_66', 'topic_cross_67', 'topic_cross_68', 'topic_cross_69', 'topic_cross_70',
	            'topic_cross_71', 'topic_cross_72', 'topic_cross_73', 'topic_cross_74', 'topic_cross_75',
	            'topic_cross_76', 'topic_cross_77', 'topic_cross_78', 'topic_cross_79', 'topic_cross_80',
	            'topic_cross_81', 'topic_cross_82', 'topic_cross_83', 'topic_cross_84', 'topic_cross_85',
	            'topic_cross_86', 'topic_cross_87', 'topic_cross_88', 'topic_cross_89', 'topic_cross_90',
	            'topic_cross_91', 'topic_cross_92', 'topic_cross_93', 'topic_cross_94', 'topic_cross_95',
	            'topic_cross_96', 'topic_cross_97', 'topic_cross_98', 'topic_cross_99', 'topic_cross_100',
	            'topic_cross_101', 'topic_cross_102', 'topic_cross_103', 'topic_cross_104', 'topic_cross_105',
	            'topic_cross_106', 'topic_cross_107', 'topic_cross_108', 'topic_cross_109', 'topic_cross_110',
	            'topic_cross_111', 'topic_cross_112', 'topic_cross_113', 'topic_cross_114', 'topic_cross_115',
	            'topic_cross_116', 'topic_cross_117', 'topic_cross_118', 'topic_cross_119', 'topic_cross_120',
	            'topic_cross_121', 'topic_cross_122', 'topic_cross_123', 'topic_cross_124', 'topic_cross_125',
	            'topic_cross_126', 'topic_cross_127', 'topic_cross_128', 'topic_cross_129', 'topic_cross_130',
	            'topic_cross_131', 'topic_cross_132', 'topic_cross_133', 'topic_cross_134', 'topic_cross_135',
	            'topic_cross_136', 'topic_cross_137', 'topic_cross_138', 'topic_cross_139', 'topic_cross_140',
	            'topic_cross_141', 'topic_cross_142', 'topic_cross_143', 'topic_cross_144', 'topic_cross_145',
	            'topic_cross_146', 'topic_cross_147', 'topic_cross_148', 'topic_cross_149']

	#limit_index += ['count_authorid_paperid','count_author_paperid']
	#limit_index += orig_index
	#limit_index += lda_index
	limit_index += lda_cross_index

	(samples,responses,is_class) = read_data("train_data_all.csv", limit_index=limit_index)
	print("Using {} CPUs".format(multiprocessing.cpu_count()))

	#This parameter works for development environment
	#classifier = sklearn.ensemble.AdaBoostClassifier(
	#	n_estimators = 50,
	classifier = sklearn.ensemble.RandomForestClassifier(
		n_estimators = 150,
		criterion = 'entropy',
		#max_features = 50,
		n_jobs = multiprocessing.cpu_count(),
		verbose = 1
	)
	#)

	classifier.fit(samples, responses)
	ret = classifier.score(samples, responses)
	print("Train score: {}".format(ret))
	important = classifier.feature_importances_
	print("Feature score: ")
	for (name,x) in zip(limit_index[1:], important):
		print("{}: {}".format(name,x))

	(tests,responses,is_class) = read_data("test_data_all.csv", limit_index=limit_index)
	predict_result = classifier.predict_proba(tests)
	label = read_index("test_index.csv")
	print("result_len: {}, label_len: {}".format(len(predict_result), len(label)))

	score_dict = dict()
	for (prob, key) in zip(predict_result, label):
		score_dict[key] = prob

	submit("Test.csv", "submit.csv", score_dict)

def add_column(orig,orig_index,new,new_file, new_column):
	label = read_index(orig_index)
	swapped_label = [ (y,x) for (x,y) in label]

	with open(orig, 'r', encoding='utf-8') as read_file:
		reader = csv.reader(read_file)
		column = reader.__next__()

		new_data = load_single_file(new, limit_keys=set(swapped_label)) #paper,author
		with open(new_file, 'w', encoding='utf-8') as write_file:
			writer = csv.writer(write_file)

			column += new_column
			writer.writerow(column)

			for (line,(author_id, paper_id)) in zip(reader, label):
				var = new_data[(paper_id,author_id)]
				for new_col in new_column:
					line.append(var[new_col])
				writer.writerow(line)
	pass

if __name__ == '__main__':
	main()
	exit()
	add_column('test_data.csv','test_index.csv','paper_author_topic_all.csv','test_data_all.csv',
	           ['topic_dot','has_topic_dot','topic_cross_0',
	            'topic_cross_1', 'topic_cross_2', 'topic_cross_3', 'topic_cross_4', 'topic_cross_5',
	            'topic_cross_6', 'topic_cross_7', 'topic_cross_8', 'topic_cross_9', 'topic_cross_10',
	            'topic_cross_11', 'topic_cross_12', 'topic_cross_13', 'topic_cross_14', 'topic_cross_15',
	            'topic_cross_16', 'topic_cross_17', 'topic_cross_18', 'topic_cross_19', 'topic_cross_20',
	            'topic_cross_21', 'topic_cross_22', 'topic_cross_23', 'topic_cross_24', 'topic_cross_25',
	            'topic_cross_26', 'topic_cross_27', 'topic_cross_28', 'topic_cross_29', 'topic_cross_30',
	            'topic_cross_31', 'topic_cross_32', 'topic_cross_33', 'topic_cross_34', 'topic_cross_35',
	            'topic_cross_36', 'topic_cross_37', 'topic_cross_38', 'topic_cross_39', 'topic_cross_40',
	            'topic_cross_41', 'topic_cross_42', 'topic_cross_43', 'topic_cross_44', 'topic_cross_45',
	            'topic_cross_46', 'topic_cross_47', 'topic_cross_48', 'topic_cross_49', 'topic_cross_50',
	            'topic_cross_51', 'topic_cross_52', 'topic_cross_53', 'topic_cross_54', 'topic_cross_55',
	            'topic_cross_56', 'topic_cross_57', 'topic_cross_58', 'topic_cross_59', 'topic_cross_60',
	            'topic_cross_61', 'topic_cross_62', 'topic_cross_63', 'topic_cross_64', 'topic_cross_65',
	            'topic_cross_66', 'topic_cross_67', 'topic_cross_68', 'topic_cross_69', 'topic_cross_70',
	            'topic_cross_71', 'topic_cross_72', 'topic_cross_73', 'topic_cross_74', 'topic_cross_75',
	            'topic_cross_76', 'topic_cross_77', 'topic_cross_78', 'topic_cross_79', 'topic_cross_80',
	            'topic_cross_81', 'topic_cross_82', 'topic_cross_83', 'topic_cross_84', 'topic_cross_85',
	            'topic_cross_86', 'topic_cross_87', 'topic_cross_88', 'topic_cross_89', 'topic_cross_90',
	            'topic_cross_91', 'topic_cross_92', 'topic_cross_93', 'topic_cross_94', 'topic_cross_95',
	            'topic_cross_96', 'topic_cross_97', 'topic_cross_98', 'topic_cross_99', 'topic_cross_100',
	            'topic_cross_101', 'topic_cross_102', 'topic_cross_103', 'topic_cross_104', 'topic_cross_105',
	            'topic_cross_106', 'topic_cross_107', 'topic_cross_108', 'topic_cross_109', 'topic_cross_110',
	            'topic_cross_111', 'topic_cross_112', 'topic_cross_113', 'topic_cross_114', 'topic_cross_115',
	            'topic_cross_116', 'topic_cross_117', 'topic_cross_118', 'topic_cross_119', 'topic_cross_120',
	            'topic_cross_121', 'topic_cross_122', 'topic_cross_123', 'topic_cross_124', 'topic_cross_125',
	            'topic_cross_126', 'topic_cross_127', 'topic_cross_128', 'topic_cross_129', 'topic_cross_130',
	            'topic_cross_131', 'topic_cross_132', 'topic_cross_133', 'topic_cross_134', 'topic_cross_135',
	            'topic_cross_136', 'topic_cross_137', 'topic_cross_138', 'topic_cross_139', 'topic_cross_140',
	            'topic_cross_141', 'topic_cross_142', 'topic_cross_143', 'topic_cross_144', 'topic_cross_145',
	            'topic_cross_146', 'topic_cross_147', 'topic_cross_148', 'topic_cross_149'])
	add_column('train_data.csv','train_index.csv','paper_author_topic_all.csv','train_data_all.csv',
	           ['topic_dot','has_topic_dot','topic_cross_0',
	            'topic_cross_1', 'topic_cross_2', 'topic_cross_3', 'topic_cross_4', 'topic_cross_5',
	            'topic_cross_6', 'topic_cross_7', 'topic_cross_8', 'topic_cross_9', 'topic_cross_10',
	            'topic_cross_11', 'topic_cross_12', 'topic_cross_13', 'topic_cross_14', 'topic_cross_15',
	            'topic_cross_16', 'topic_cross_17', 'topic_cross_18', 'topic_cross_19', 'topic_cross_20',
	            'topic_cross_21', 'topic_cross_22', 'topic_cross_23', 'topic_cross_24', 'topic_cross_25',
	            'topic_cross_26', 'topic_cross_27', 'topic_cross_28', 'topic_cross_29', 'topic_cross_30',
	            'topic_cross_31', 'topic_cross_32', 'topic_cross_33', 'topic_cross_34', 'topic_cross_35',
	            'topic_cross_36', 'topic_cross_37', 'topic_cross_38', 'topic_cross_39', 'topic_cross_40',
	            'topic_cross_41', 'topic_cross_42', 'topic_cross_43', 'topic_cross_44', 'topic_cross_45',
	            'topic_cross_46', 'topic_cross_47', 'topic_cross_48', 'topic_cross_49', 'topic_cross_50',
	            'topic_cross_51', 'topic_cross_52', 'topic_cross_53', 'topic_cross_54', 'topic_cross_55',
	            'topic_cross_56', 'topic_cross_57', 'topic_cross_58', 'topic_cross_59', 'topic_cross_60',
	            'topic_cross_61', 'topic_cross_62', 'topic_cross_63', 'topic_cross_64', 'topic_cross_65',
	            'topic_cross_66', 'topic_cross_67', 'topic_cross_68', 'topic_cross_69', 'topic_cross_70',
	            'topic_cross_71', 'topic_cross_72', 'topic_cross_73', 'topic_cross_74', 'topic_cross_75',
	            'topic_cross_76', 'topic_cross_77', 'topic_cross_78', 'topic_cross_79', 'topic_cross_80',
	            'topic_cross_81', 'topic_cross_82', 'topic_cross_83', 'topic_cross_84', 'topic_cross_85',
	            'topic_cross_86', 'topic_cross_87', 'topic_cross_88', 'topic_cross_89', 'topic_cross_90',
	            'topic_cross_91', 'topic_cross_92', 'topic_cross_93', 'topic_cross_94', 'topic_cross_95',
	            'topic_cross_96', 'topic_cross_97', 'topic_cross_98', 'topic_cross_99', 'topic_cross_100',
	            'topic_cross_101', 'topic_cross_102', 'topic_cross_103', 'topic_cross_104', 'topic_cross_105',
	            'topic_cross_106', 'topic_cross_107', 'topic_cross_108', 'topic_cross_109', 'topic_cross_110',
	            'topic_cross_111', 'topic_cross_112', 'topic_cross_113', 'topic_cross_114', 'topic_cross_115',
	            'topic_cross_116', 'topic_cross_117', 'topic_cross_118', 'topic_cross_119', 'topic_cross_120',
	            'topic_cross_121', 'topic_cross_122', 'topic_cross_123', 'topic_cross_124', 'topic_cross_125',
	            'topic_cross_126', 'topic_cross_127', 'topic_cross_128', 'topic_cross_129', 'topic_cross_130',
	            'topic_cross_131', 'topic_cross_132', 'topic_cross_133', 'topic_cross_134', 'topic_cross_135',
	            'topic_cross_136', 'topic_cross_137', 'topic_cross_138', 'topic_cross_139', 'topic_cross_140',
	            'topic_cross_141', 'topic_cross_142', 'topic_cross_143', 'topic_cross_144', 'topic_cross_145',
	            'topic_cross_146', 'topic_cross_147', 'topic_cross_148', 'topic_cross_149'])
