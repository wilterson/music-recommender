import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pickle

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


def load_model():
    model = None

    with open('./similarity_01.pkl', 'rb') as f:
        model = pickle.load(f)

    return model

# def get_recommendations(audio_features):
#     model = load_model()

#     if not model:
#         return None

#     print('FEATURES: ', audio_features)
    # recommendations = model.predict(input_data)
    # return prediction


def get_recommendations(audio_features):
    with open('similarity_full_features.pkl', 'rb') as f:
        get_similarities = pickle.load(f)

    # get_similarities = pickle.load(open('similarity_01.pkl', 'rb'))
    recommendations = get_similarities(audio_features)

    print(recommendations)


def get_recommendations_by_genre(genre):
    get_similarities_by_genre = pickle.load(open('notebooks/similarity.pkl', 'rb'))
    recommendations = get_similarities_by_genre(genre)

    print('BY GENRE: ', recommendations)


def app():
    # Page Metadata
    st.set_page_config(page_title="Music Recommendations", page_icon=":musical_note:")
    st.write(f"<style>{CSS}</style>", unsafe_allow_html=True)
    st.title('Music Recommendation')

    # Login
    session_state = SessionState(token=None)
    sp = login()

    if not sp:
        st.warning("Por favor, faça login para continuar.")
        return

    if st.button('Get Recommendations'):  # Show button after successful login
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

            # st.write(f"Name: {track['track']['name']}")
            # st.write(f"Artist: {track['track']['artists'][0]['name']}")
            # st.write(f"Album: {track['track']['album']['name']}")
            # st.write(f"Popularity: {track['track']['popularity']}")
            # st.write(f"Acousticness: {track['audio_features']['acousticness']}")
            # st.write(f"Danceability: {track['audio_features']['danceability']}")
            # st.write(f"Energy: {track['audio_features']['energy']}")
            # st.write(f"Instrumentalness: {track['audio_features']['instrumentalness']}")
            # st.write(f"Liveness: {track['audio_features']['liveness']}")
            # st.write(f"Loudness: {track['audio_features']['loudness']}")
            # st.write(f"Speechiness: {track['audio_features']['speechiness']}")
            # st.write(f"Valence: {track['audio_features']['valence']}")
            # st.write('---')

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

        print('\n\nFEATURES: ', features)

        # recommendations = get_recommendations([features])
        recommendations = get_recommendations(features)

# Run Streamlit app
if __name__ == '__main__':
    app()
