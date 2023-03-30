# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 20:13:45 2023

@author: WELCOME
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer

import dill

def convert_int(x):
    try:
        return int(x)
    except:
        return 0
    
class mo:
    def __init__(self,df,tfidf,indices) -> None:
        self.df=df
        self.tfidf=tfidf
        self.indices=indices

    def content_recommender(self,title):
        import pandas as pd
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        from ast import literal_eval
        from sklearn.feature_extraction.text import TfidfVectorizer
        idx = self.indices[title]
        tf_title=self.tfidf[idx,:]
        sim_scores = list(enumerate(cosine_similarity(self.tfidf,tf_title)))
        sim_sorted = sorted(sim_scores,key=lambda x:x[1],reverse=True)
        sim_rec = sim_sorted[1:11]
        movie_indices = [i[0] for i in sim_rec]
        return self.df['title'].iloc[movie_indices]
    
if __name__=='__main__':
    df = pd.read_csv('movies_metadata.csv')
    df = df[['title','genres', 'release_date', 'runtime', 'vote_average', 'vote_count','overview','id']]
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    df['year'] = df['year'].apply(convert_int)
    df['genres'] = df['genres'].fillna('[]')
    df['genres'] = df['genres'].apply(literal_eval)
    df['genres'] = df['genres'].apply(lambda x: [i['name'].lower() for i in x] if isinstance(x, list) else [])
    tfidf = TfidfVectorizer(stop_words='english')
    df['overview'] = df['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df['overview'])
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    obj=mo(df,tfidf_matrix,indices)
    dill.dump(obj,open('model.pkl','wb'))


