import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import dill

class SimilarityModel:
    def __init__(self):
        self.df_data = pd.read_csv('https://drive.google.com/uc?export=download&id=1tdnYgbK3-OJeeMK-QrW-ha6WgXcC79hE', low_memory=False, encoding='latin-1')

        name_artist = ['name','artists']
        self.df_data = self.df_data.drop_duplicates(subset=name_artist,keep='last')
        self.df = self.df_data[['acousticness','danceability','energy','instrumentalness', 'liveness', 'loudness', 'speechiness','valence']]

    def get_similarities(self, vetor):
        input_vector = np.array([vetor])
        cosine_similarities = cosine_similarity(self.df, input_vector)
        df_retorno_genres = self.df.iloc[cosine_similarities[:,0].argsort()[::-1][:30]].merge(self.df_data[['id','name','artists','popularity']],how = 'inner',left_index=True,right_index=True).sort_values('popularity',ascending=False).head(10)

        return df_retorno_genres

if __name__ == '__main__':
    model = SimilarityModel()

    with open('similarity_full_features.pkl', 'wb') as f:
        dill.dump(model.get_similarities, f)