#-*- encoding:utf-8 -*-
from __future__ import print_function
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


if __name__ == '__main__': 
	text = codecs.open('input.txt', 'r', 'utf-8').read()
	tr4s = TextRank4Sentence()
	tr4s.analyze(text=text, lower=True, source = 'all_filters')

	print( '摘要：' )
	for item in tr4s.get_key_sentences(num=5):
	    print('Sent Idx: {}, Weight: {:.4f}\n{}\n'.format(item.index, item.weight, item.sentence))  # index是語句在文本中位置，weight是權重
