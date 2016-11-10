
[1] Generate the inverse index list from provided documents

task1.py: corpus.txt >> indexTC.txt

[2] Generate the ranking result through 3 methods: VSM1, VSM2, BM25

VSM1,	task2a.py: indexTC.txt >> resultsVSM1.txt

VSM2,	task2b.py: indexTC.txt >> resultsVSM2.txt

BM25,	task2c.py: indexTC.txt >> resultsBM25.txt

[3] Generate the comparison result from previous rankings

task3.py

{	'tausVSM1_VSM2': 
	{u'1': 0.6214896214896215, u'3': 0.8422161999397771, u'2': 0.6765822784810127, u'4': 0.5803702615339407}, 
	'tausVSM2_BM25': 
	{u'1': 0.3696969696969697, u'3': 0.3377630121816168, u'2': 0.07393483709273183, u'4': 0.14950166112956811}, 
	'tausVSM1_BM25': 
	{u'1': 0.3593220338983051, u'3': 0.36268343815513626, u'2': 0.21393034825870647, u'4': 0.2631578947368421}
}

[4] Generate the inverse index list from Wikipedia

task_extra.py: dic_html.txt >> wiki_index.txt
