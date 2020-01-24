# LDA
Topic Modelling RMP

Topic modelling the RateMyProfessor.com (RMP ) reviews and rating attributes after web scraping the data. I used the comment corpus  to answer the following question:  what words do students use to describe their professors?.I modeled the reviews using Latent Dirichlet Allocation (LDA) and  run several regression models to analyze if there are statistically significant factors that influence the overall rating.

Data Collection was done using python libraries and LDA was executed using the GENSIM implementation. NLTK lemmatization and stop words removal were conducted as part of the initial preprocessing. Coherence score was calculated for comparing between LDA models and for identifying hyper parameters used in LDA.
  
The project builds on the studies uncovering the seemingly existing gender bias, by analyzing the professor description through comments and performance rating, for a data-set consisting of Ontario's Economics professors. We expected to identify gender-specific aspects or themes, which underline the comment corpus, by applying topic modeling algorithm LDA. When we correlated them with numerical ratings, which constitute the RMP data-set, we found statistically significantly higher ratings for male professors compared to female professors.
