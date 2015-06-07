import cv2
import cv2.ocl
import cv2.ml
import csv
import numpy
import sys

def enableOpenCL(verbose = False):
	has_opencl = cv2.ocl.haveOpenCL()
	if(verbose):
		print("Have openCL? {0}".format(has_opencl))
	if has_opencl:
		return cv2.ocl.useOpenCL()
	else:
		return False

def read_data(filename, result_type = cv2.ml.VAR_CATEGORICAL):
	with open(filename, 'r', encoding='utf-8') as read_file:
		samples = []
		responses = []
		reader = csv.reader(read_file)
		column = reader.__next__()

		target_id = -1
		var_type = []
		for i in range(len(column)):
			if column[i].lower() == "target":
				target_id = i
				#var_type.append(cv2.ml.VAR_CATEGORICAL)
			elif 'has_' in column[i] or 'type_' in column[i]:
				var_type.append(cv2.ml.VAR_CATEGORICAL)
			else:
				var_type.append(cv2.ml.VAR_NUMERICAL)
		var_type.append(result_type)

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
		result_dtype = numpy.int32
		if(result_type == cv2.ml.VAR_NUMERICAL):
			result_dtype = numpy.float32
		return (numpy.array(samples, dtype=numpy.float32),
		        numpy.array(responses, dtype=result_dtype),
		        numpy.array(var_type, dtype=numpy.int32))

def categorize_data(matrix, responses, var_type, K, center_dict = None):
	todo_list = []
	for (i,type) in zip(range(len(var_type)), var_type):
		if type == cv2.ml.VAR_NUMERICAL:
			todo_list.append(i)
	#ret_mat = matrix.astype(numpy.int32, copy=True)
	print(todo_list)
	do_kmean = False
	if center_dict == None:
		do_kmean = True
		center_dict = {}
	for i in todo_list:
		col = matrix[:,i]
		#print(matrix[:,i])
		if do_kmean:
			_temp = []
			for _i in range(len(col)):
				_temp.append([0])
			best = numpy.array(_temp)
			(error, matching, center) = cv2.kmeans(data=col, K=K, bestLabels=best,
			                    criteria=(cv2.TermCriteria_MAX_ITER,len(col), 0.0001),
			                    attempts=1, flags=cv2.KMEANS_PP_CENTERS)
			for _i in range(len(col)):
				matrix[_i,i] = best[_i]
			center_dict[i] = center
		else:
			centers = center_dict[i]
			for _i in range(len(col)):
				error = float('inf')
				prev_val = matrix[_i,i]
				index = (numpy.abs(centers-prev_val)).argmin()
				matrix[_i,i] = index

		#print(matrix[:,i])
		var_type[i] = cv2.ml.VAR_CATEGORICAL
	print(matrix)
	return (matrix, responses, var_type, center_dict)

def main():

	result_type = cv2.ml.VAR_CATEGORICAL
	print(enableOpenCL(verbose = True))
	(samples,responses,var_type) = read_data('train_data.csv', result_type=result_type)
	#(samples,responses,var_type, center_dict) = categorize_data(samples,responses,var_type, 10)


	print(var_type)
	train_data = cv2.ml.TrainData_create(samples, cv2.ml.ROW_SAMPLE, responses)
	print(train_data)


	train_model = cv2.ml.Boost_create()

	train_model.setBoostType(cv2.ml.BOOST_REAL)
	train_model.setWeightTrimRate(0.999)
	train_model.setRegressionAccuracy(0.999)

	train_model.setMaxCategories(1500)
	train_model.setMaxDepth(5)

	ret = train_model.train(train_data)
	print(ret)
	print('isClassifier? {}'.format(train_model.isClassifier()))
	print('Boost model: {}'.format(train_model.getBoostType()))
	print('Weak count: {}'.format(train_model.getWeakCount()))
	print('Weight trim rate: {}'.format(train_model.getWeightTrimRate()))
	print('Variable count: {}'.format(train_model.getVarCount()))

	#file_storage = cv2.FileStorage('train_data', flags=cv2.FileStorage_WRITE, encoding='utf-8')
	#print(file_storage)
	#file_storage.writeObj('train_model', train_model)

#def main2():
	#file_storage = cv2.FileStorage('train_data', flags=cv2.FileStorage_READ, encoding='utf-8')
	#train_model = file_storage.readObj()
	print(train_model)
	(tests,responses, var_type) = read_data('test_data.csv', result_type=result_type)
	#(tests,responses,var_type, center_dict) = categorize_data(samples,responses,var_type, 10, center_dict=center_dict)
	print(var_type)

	err = train_model.predict(tests)
	print("Error: {}".format(err[0]))
	print(err[1])
	print(len(err[1]))

	return
	for test in tests:
		x = [test.tolist()]
		print (x)
		err = train_model.predict(test)
		print("Error: {}".format(err[0]))
		print(err[1])
	#for x in err[1]:
	#	print(x)

if __name__ == '__main__':
	main()
	#main2()