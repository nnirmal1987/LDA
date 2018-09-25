import gensim
from gensim import corpora
from gensim.models import CoherenceModel
import system 
import pickle
import os
from gensim.corpora.dictionary import Dictionary
import sys

# Calculating coherence score (C_V) for comparing LDA models 
def lda_work(k,alpha,eta):
    texts=[]
    doc=[]
    texts=[]               
    texts = pickle.load(open('textsuni.pickle', 'rb'))
    dictionary = Dictionary(texts)
    print(len(dictionary))
    corpus = [dictionary.doc2bow(text) for text in texts]
    model = gensim.models.ldamodel.LdaModel(corpus,id2word=dictionary,alpha=alpha,eta=eta,num_topics=k,passes=10)
    coherencemodel = CoherenceModel(model=model,texts=texts,corpus=corpus,dictionary=dictionary,coherence='c_v',topn=7)
    coherence_values=coherencemodel.get_coherence()
    fpnter=open('file\\'+'coherence '+str(k)+'_'+str(alpha)+'_'+str(eta)+'.txt','w')
    fpnter.write('coherence value='+''+str(coherence_values)+'\n'+'topics='+''+str(k)+'\n'+'alpha='+''+str(alpha)+'\n'+'eta='+''+str(eta)) 
	fpnter.close()
    

if __name__ == "__main__":
    lda_work(int(sys.argv[1]), float(sys.argv[2]),float(sys.argv[3]))