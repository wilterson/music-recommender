import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import pandas as pd
import dill

from sklearn.metrics.pairwise import cosine_similarity

import credentials

CSS = """
button {
    background-color: #0e1117;
    color: white;
    padding: 0.75rem;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: bold;
    text-align: center;
    transition: background-color 0.15s ease-in-out;
}
button:hover, button:focus {
    background-color: #1db954;
    color: white !important;
    border-color: rgb(255, 255, 255) !important;
    transition: background-color 0.15s ease-in-out;
}
button:active {
    background-color: #0e1117;
    color: black !important;
    transition: background-color 0.15s ease-in-out;
    border-color: rgb(255, 255, 255) !important;
    background-color: rgb(255, 255, 255) !important;
}
"""

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def login():
    session_state = SessionState(token=None)

    if session_state.token is None:
        sp_oauth = SpotifyOAuth(
            client_id=credentials.SPOTIFY_CLIENT_ID,
            client_secret=credentials.SPOTIFY_CLIENT_SECRET,
            redirect_uri=credentials.APP_REDIRECT_URI,
            scope='user-library-read',
            cache_path='.spotifycache'
        )

        auth_url = sp_oauth.get_authorize_url()
        st.write(f"[Login com Spotify]({auth_url})")

        code = st.experimental_get_query_params().get("code", None)

        if code:
            token_info = sp_oauth.get_access_token(code)

            if token_info is not None:
                session_state.token = token_info['access_token']
                sp = spotipy.Spotify(auth=session_state.token)

                return sp
            else:
                st.write('Falha na autenticação. Tente novamente.')

        else:
            return None

    else:
        sp = spotipy.Spotify(auth=session_state.token)
        session_state.token = sp_oauth.refresh_access_token(session_state.token)['access_token']

        return sp


def get_recommendations(audio_features):
    model_file = 'similarity_full_features.pkl'

    with open(model_file, 'rb') as f:
        get_similarities = dill.load(f)

    recommendations = get_similarities(audio_features)

    return recommendations


def get_recommendations_by_genre(genre):
    model_file = 'similarity_genres.pkl'

    with open(model_file, 'rb') as f:
        get_similarities = dill.load(f)

    recommendations = get_similarities(genre)

    return recommendations

def get_tracks_info(tracks):
    for i, row in tracks.iterrows():
        track_info = sp.track(row['id'], market='BR')

        tracks.loc[i, 'preview_url'] = track_info.get('preview_url', '')
        tracks.loc[i, 'image'] = track_info['album']['images'][0]['url']

    return tracks


def display_tracks(recommendations):
    for _, row in recommendations.iterrows():
        if pd.isna(row).any():
            continue

        image_url = row.get('image', '')
        if image_url:
            st.image(image_url, width=150)

        st.write(row['name'])

        artists = row.get('artists', '')
        if artists:
            st.write(f"Artist: {artists}")

        album_name = row.get(' album_name', '')
        if album_name:
            st.write(f"Album: {album_name}")

        popularity = row.get('popularity', '')
        if popularity:
            st.write(f"Popularity: {popularity}")

        preview_url = row.get('preview_url', '')
        if preview_url:
            st.audio(preview_url, format='audio/mp3', start_time=0)

        track_id = row.get('id', '')
        if track_id:
            st.write(f"[Ouvir com Spotify](https://open.spotify.com/track/{track_id})")

        st.write('---')


def app():
    # Page Metadata
    st.set_page_config(page_title="Music Recommendations", page_icon=":musical_note:")
    st.write(f"<style>{CSS}</style>", unsafe_allow_html=True)
    st.title('Music Recommendation')

    # Set up the tabs
    tabs = ["Recomendações por Gênero", "Recomendações por likes no Spotify"]
    active_tab = st.sidebar.radio("Select Tab", tabs)


    # Login
    session_state = SessionState(token=None)
    sp = login()

    if not sp:
        st.warning("Por favor, faça login para continuar.")
        return

    if active_tab == "Recomendações por likes no Spotify":
        if st.button('Get Recommendations'):  # Show button after successful login
            with st.spinner('Loading...'):
                results = sp.current_user_saved_tracks(limit=5)
                tracks = results['items']

                track_ids = []

                for track in tracks:
                    track_ids.append(track['track']['id'])

                track_features = sp.audio_features(track_ids)

                features_dict = {}
                for feature in track_features:
                    features_dict[feature['id']] = feature

                for track in tracks:
                    track_id = track['track']['id']
                    if track_id in features_dict:
                        track['audio_features'] = features_dict[track_id]

                features = [
                    tracks[0]['audio_features']['acousticness'],
                    tracks[0]['audio_features']['danceability'],
                    tracks[0]['audio_features']['energy'],
                    tracks[0]['audio_features']['instrumentalness'],
                    tracks[0]['audio_features']['liveness'],
                    tracks[0]['audio_features']['loudness'],
                    tracks[0]['audio_features']['speechiness'],
                    tracks[0]['audio_features']['valence'],
                ]

                # Code to fetch recommendations
                recommendations = get_recommendations(features)

                for i, row in recommendations.iterrows():
                    track_info = sp.track(row['id'], market='BR')

                    recommendations.loc[i, 'preview_url'] = track_info.get('preview_url', '')
                    recommendations.loc[i, 'image'] = track_info['album']['images'][0]['url']

                st.title('Musicas Recomendadas para você:')
                st.subheader('Baseado nas músicas que você curtiu no Spotify')

                display_tracks(recommendations)

    if active_tab == "Recomendações por Gênero":
        genres = ['A Cappella', 'Rock', 'Pop', 'Jazz', 'Blues', 'Classical', 'Metal', 'Indie', 'Opera', 'Remix', 'Sertanejo']
        selected_genre = st.selectbox('Select a genre:', genres)

        if st.button('Get Recommendations by Genre'):
            with st.spinner('Loading...'):
                recommendations = get_recommendations_by_genre(selected_genre)

                # recommendations = get_tracks_info(recommendations)
                for i, row in recommendations.iterrows():
                    track_info = sp.track(row['id'], market='BR')

                    recommendations.loc[i, 'preview_url'] = track_info.get('preview_url', '')
                    recommendations.loc[i, 'image'] = track_info['album']['images'][0]['url']

                st.title('Musicas Recomendadas para você:')
                st.subheader('Baseado no gênero selecionado')

                display_tracks(recommendations)

# Run Streamlit app
if __name__ == '__main__':
    app()
