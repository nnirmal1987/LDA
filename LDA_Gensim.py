import nltk
from nltk.tokenize import RegexpTokenizer
import gensim
from gensim import corpora
import json
import os
from nltk.corpus import stopwords 
from gensim.models import Phrases
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from gensim.models import Phrases
from gensim.models.phrases import Phraser
en_stop = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')

tifinal=[]
bifinal=[]
texts=[]
doc=[]

#Read scraped professor details including rating comments
list = os.listdir(os.getcwd())                
for file in list:
        if(file.startswith('rmp_econ_gender')):
             for i in range(0, 1109):
                fle= json.loads(open("rmp_econ_gender.txt","r").read())
                doc.append(fle[i]["finalreview"])
        else: 
            continue
 
# Removing user defined stopwords and including some semantically significant word of length < 3
lstp=[]
words_list3=[]
fp=open("new_stp.txt","r")
fp1=open("word_list3.txt","r")
lstp=fp.read().splitlines()
words_list3=fp1.read().splitlines()
fp.close()
fp1.close()

# Text preprocessing
for i in doc:
                raw = i.lower()       
                tokens = tokenizer.tokenize(str(raw))              
                stopped_tokens = [i for i in tokens if i not in en_stop]
                lemmatizer = WordNetLemmatizer()             
                lemmatized_tokens=[lemmatizer.lemmatize(i) for i in stopped_tokens] 
                cleaned_tokens = [i for i in lemmatized_tokens if i not in lstp]  
                tokens_digit = [i for i in cleaned_tokens if not i.isdigit()]  
                tokens_len =[i for i in tokens_digit if len(i)>2]
                for i in tokens_len:
                    if(len(i)==3 and i not in words_list3):
                        tokens_len.remove(i)
                texts.append(tokens_len)


d=defaultdict(int)
for lister in texts:
    for  item in lister:
        d[item]+=1

tokens=[key for key,value in d.items() if value>2]
texts = [[word.encode('utf-8') for word in document if word in tokens] for document in texts]

# Add bigrams to corpus
bigram = Phrases(texts,min_count=3,delimiter=b'_',threshold=5)
for token in texts:
    bigrams_ = [b.encode('utf-8') for b in bigram[token]if b.count('_') == 1]
    bifinal.append(bigrams_)
for value in bifinal:
    if not value:
        continue
    else:
        texts.append(value)
		
# Add trigrams to corpus	
trigram = Phrases(bigram[texts],min_count=2,delimiter=b'_',threshold=3)
for token in texts:
    trigrams_=[t.encode('utf-8') for t in trigram[bigram[token]]if t.count('_') == 2]
    tifinal.append(trigrams_)
for value in tifinal:
    if not value:
        continue
    else:
        texts.append(value)

#Creating dictionary and corpus
dictionary=corpora.Dictionary(texts)
print(len(dictionary))
corpus = [dictionary.doc2bow(text) for text in texts]

#Running Gensim LDA for fetching the topics
lda_model = gensim.models.ldamodel.LdaModel(corpus,id2word = dictionary,num_topics=10,alpha='auto',chunksize = 100,update_every=1,iterations=100,passes=20)
lda_model.print_topics(num_words=20)

#Fetching topic distribution of each document in the corpus
for i in range(len(corpus)):
        txt=lda_model[corpus[i]]
        d=dict(txt)
        trt=[v for (k, v) in sorted(txt)]
        print(max(d, key=d.get),max(trt))

