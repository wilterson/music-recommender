import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import dill

class SimilarityModelGenre:
    def __init__(self):
        self.df_data_by_genres = pd.read_csv('https://drive.google.com/uc?export=download&id=12lqn5lD6x5Yh6mezlg6TQ60YA-Pn8aeV', low_memory=False, encoding='latin-1')
        self.df_data = pd.read_csv('https://drive.google.com/uc?export=download&id=1tdnYgbK3-OJeeMK-QrW-ha6WgXcC79hE', low_memory=False, encoding='latin-1')

        name_artist = ['name','artists']
        self.df_data = self.df_data.drop_duplicates(subset=name_artist,keep='last')
        self.df_music = self.df_data[['acousticness','danceability','energy','instrumentalness', 'liveness', 'loudness', 'speechiness','valence']]

    def get_similarities(self, genre):
        print('DATAFRAME: ', self.df_data_by_genres.head())

        music_genre = self.df_data_by_genres[self.df_data_by_genres['genres'] == genre.lower()]
        input_vector = music_genre[['acousticness','danceability','energy','instrumentalness', 'liveness', 'loudness', 'speechiness','valence']]
        cosine_similarities = cosine_similarity(self.df_music, input_vector)
        df_retorno_genres = self.df_music.iloc[cosine_similarities[:,0].argsort()[::-1][:30]].merge(self.df_data[['id','name','artists','popularity']],how = 'inner',left_index=True,right_index=True).sort_values('popularity',ascending=False).head(10)

        return df_retorno_genres

if __name__ == '__main__':
    model = SimilarityModelGenre()

    with open('similarity_genres.pkl', 'wb') as f:
        dill.dump(model.get_similarities, f)