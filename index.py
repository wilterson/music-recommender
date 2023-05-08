import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def app():
    st.title('Music Recommendation')

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
        st.write(f"[Autorizar]({auth_url}) acesso a minha conta Spotify")
        code = st.experimental_get_query_params().get("code", None)

        if code:
            token_info = sp_oauth.get_access_token(code)
            session_state.token = token_info['access_token']
            sp = spotipy.Spotify(auth=session_state.token)

            results = sp.current_user_saved_tracks(limit=5)
            tracks = results['items']

            for track in tracks:
                st.write(f"Name: {track['track']['name']}")
                st.write(f"Artist: {track['track']['artists'][0]['name']}")
                st.write(f"Album: {track['track']['album']['name']}")
                st.write(f"Added at: {track['added_at']}")
                st.write('---')

# Run Streamlit app
if __name__ == '__main__':
    app()
