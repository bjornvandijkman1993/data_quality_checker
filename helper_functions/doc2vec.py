import pandas as pd
import streamlit as st

from gensim import utils
import gensim.parsing.preprocessing as gsp

from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.parsing.preprocessing import preprocess_string
from sklearn.base import BaseEstimator
from sklearn import utils as skl_utils
from tqdm import tqdm

import multiprocessing
import numpy as np

from sklearn.neural_network import MLPRegressor
from scipy.spatial.distance import cosine

def doc2vec(df, feature_to_vectorize, other_column):

    df = df[[feature_to_vectorize, other_column]]
    filters = [
               gsp.strip_tags,
               gsp.strip_punctuation,
               gsp.strip_multiple_whitespaces,
               gsp.strip_numeric,
               gsp.remove_stopwords,
               gsp.strip_short,
               gsp.stem_text
              ]

    def clean_text(s):
        s = s.lower()
        s = utils.to_unicode(s)
        for f in filters:
            s = f(s)
        return s

    # title_plot_df['Plot'] = title_plot_df['Plot'].map(lambda x: clean_text(x))
    df[feature_to_vectorize] = df[feature_to_vectorize].map(lambda x: clean_text(x))


    class Doc2VecTransformer(BaseEstimator):

        def __init__(self, vector_size=100, learning_rate=0.02, epochs=20):
            self.learning_rate = learning_rate
            self.epochs = epochs
            self._model = None
            self.vector_size = vector_size
            self.workers = multiprocessing.cpu_count() - 1

        def fit(self, df_x, df_y=None):
            # tagged_x = [TaggedDocument(str(row['Plot']).split(), [index]) for index, row in df_x.iterrows()]
            tagged_x = [TaggedDocument(str(row[feature_to_vectorize]).split(), [index]) for index, row in df_x.iterrows()]

            model = Doc2Vec(documents=tagged_x, vector_size=self.vector_size, workers=self.workers)

            for epoch in range(self.epochs):
                model.train(skl_utils.shuffle([x for x in tqdm(tagged_x)]), total_examples=len(tagged_x), epochs=1)
                model.alpha -= self.learning_rate
                model.min_alpha = model.alpha

            self._model = model
            return self

        def transform(self, df_x):
            return np.asmatrix(np.array([self._model.infer_vector(str(row[feature_to_vectorize]).split())
            # return np.asmatrix(np.array([self._model.infer_vector(str(row['Plot']).split())
                                         for index, row in df_x.iterrows()]))


    doc2vec_tr = Doc2VecTransformer(vector_size=300)
    # doc2vec_tr.fit(title_plot_df)
    doc2vec_tr.fit(df)
    # doc2vec_vectors = doc2vec_tr.transform(title_plot_df)
    doc2vec_vectors = doc2vec_tr.transform(df)

    auto_encoder = MLPRegressor(hidden_layer_sizes=(
                                                     600,
                                                     150,
                                                     600,
                                                   ))
    auto_encoder.fit(doc2vec_vectors, doc2vec_vectors)
    predicted_vectors = auto_encoder.predict(doc2vec_vectors)



    def key_consine_similarity(tupple):
        return tupple[1]

    def get_computed_similarities(vectors, predicted_vectors, reverse=False):
        data_size = len(df)
        cosine_similarities = []
        for i in range(data_size):
            cosine_sim_val = (1 - cosine(vectors[i], predicted_vectors[i]))
            cosine_similarities.append((i, cosine_sim_val))

        return sorted(cosine_similarities, key=key_consine_similarity, reverse=reverse)


    similarities = []
    titles = []
    plot = []

    #def display_top_n(sorted_cosine_similarities, n=len(title_plot_df)):
    def display_top_n(sorted_cosine_similarities, n=len(df)):
        for i in range(n):
            index, consine_sim_val = sorted_cosine_similarities[i]
            titles.append(df.iloc[index, 0])
            plot.append(df.iloc[index, 1])
            similarities.append(consine_sim_val)

    sorted_cosine_similarities = get_computed_similarities(vectors=doc2vec_vectors, predicted_vectors=predicted_vectors)
    display_top_n(sorted_cosine_similarities=sorted_cosine_similarities)

    data = pd.DataFrame(
        {feature_to_vectorize + '_Doc2Vec_Score': similarities,
         other_column: plot
         })

    return data

