import sys
import lda_cache


def model_parameters_tuning_func():
    print ('PYCALLING func')
    for topic in range(5,10,1):
        for alpha in [1/round(float(topic),3), 0.01,0.04,0.08,0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
            beta=(1/float(topic))
            lda_coherence.lda_work(topic,alpha,beta)

if __name__ == '__main__':
    model_parameters_tuning_func()
    

