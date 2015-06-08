from loader import *
from create_feature import *

def main():
	total_data = load_all()
	load_title_lda(total_data)
	paper_topic(total_data)
	author_topic(total_data)
	paper_author_topic_sum(total_data)
	save_topic_sum(total_data)
	pass

if __name__ == '__main__':
	main()
