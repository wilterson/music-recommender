import numpy as np
import pandas as pd
import dill
import os

from sklearn.metrics.pairwise import cosine_similarity

def get_similarities(vetor):
    df_data = pd.read_csv('https://drive.google.com/uc?export=download&id=1tdnYgbK3-OJeeMK-QrW-ha6WgXcC79hE', low_memory=False, encoding='latin-1')
    df_data_by_artist = pd.read_csv('https://drive.google.com/uc?export=download&id=1oPnKdpQLK7CO5rUVrMwvTvQuBGSmvRLH', low_memory=False, encoding='latin-1')
    df_data_by_genres = pd.read_csv('https://drive.google.com/uc?export=download&id=12lqn5lD6x5Yh6mezlg6TQ60YA-Pn8aeV', low_memory=False, encoding='latin-1')
    df_data_by_year = pd.read_csv('https://drive.google.com/uc?export=download&id=1zZrUYorbuT5MTCrzqvJDiK-W4M48IrM_', low_memory=False, encoding='latin-1')
    df_data_w_genres = pd.read_csv('https://drive.google.com/uc?export=download&id=1fDUFtB5CG4MBnfj80q2h9r47Nlwzy9t1', low_memory=False, encoding='latin-1')

    valores_distintos = df_data.query('popularity == popularity')['popularity'].unique()
    np.sort(valores_distintos)

    name_artist = ['name','artists']
    df_data = df_data.drop_duplicates(subset=name_artist,keep='last')

    df = df_data[['acousticness','danceability','energy','instrumentalness', 'liveness', 'loudness', 'speechiness','valence']]
    # vetor['acousticness','danceability','energy','instrumentalness', 'liveness', 'loudness', 'speechiness','valence']
    input_vector = vetor
    cosine_similarities = cosine_similarity(df, input_vector)
    df_retorno_genres = df.iloc[cosine_similarities[:,0].argsort()[::-1][:30]].merge(df_data[['id','name','artists','popularity']],how = 'inner',left_index=True,right_index=True).sort_values('popularity',ascending=False).head(10)

    return df_retorno_genres

if __name__ == '__main__':
    with open('similarity_full_features.pkl', 'wb') as f:
        dill.dump(get_similarities, f)

# import numpy as np
# import pandas as pd
# import pickle
# from sklearn.metrics.pairwise import cosine_similarity

# def get_similarities(vetor):
#     df_data = pd.read_csv('https://drive.google.com/uc?export=download&id=1tdnYgbK3-OJeeMK-QrW-ha6WgXcC79hE', low_memory=False, encoding='latin-1')
#     df_data_by_artist = pd.read_csv('https://drive.google.com/uc?export=download&id=1oPnKdpQLK7CO5rUVrMwvTvQuBGSmvRLH', low_memory=False, encoding='latin-1')
#     df_data_by_genres = pd.read_csv('https://drive.google.com/uc?export=download&id=12lqn5lD6x5Yh6mezlg6TQ60YA-Pn8aeV', low_memory=False, encoding='latin-1')
#     df_data_by_year = pd.read_csv('https://drive.google.com/uc?export=download&id=1zZrUYorbuT5MTCrzqvJDiK-W4M48IrM_', low_memory=False, encoding='latin-1')
#     df_data_w_genres = pd.read_csv('https://drive.google.com/uc?export=download&id=1fDUFtB5CG4MBnfj80q2h9r47Nlwzy9t1', low_memory=False, encoding='latin-1')

#     valores_distintos = df_data.query('popularity == popularity')['popularity'].unique()
#     np.sort(valores_distintos)

#     name_artist = ['name','artists']
#     df_data = df_data.drop_duplicates(subset=name_artist,keep='last')

#     df = df_data[['acousticness','danceability','energy','instrumentalness', 'liveness', 'loudness', 'speechiness','valence']]
#     # vetor['acousticness','danceability','energy','instrumentalness', 'liveness', 'loudness', 'speechiness','valence']
#     input_vector = vetor
#     cosine_similarities = cosine_similarity(df, input_vector)
#     df_retorno_genres = df.iloc[cosine_similarities[:,0].argsort()[::-1][:30]].merge(df_data[['id','name','artists','popularity']],how = 'inner',left_index=True,right_index=True).sort_values('popularity',ascending=False).head(10)

#     return df_retorno_genres

# pickle.dump(get_similarities,open('similarity_01.pkl','wb'))
# # print(get_similarities([[0.145, 0.629, 0.657, 0.000484, 0.121, -11.251, 0.0447, 0.523]]))