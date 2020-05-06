import spotipy
import spotipy.util as util
import time
from pywinauto import Application
from spotipy.oauth2 import SpotifyClientCredentials

cid = "XXXX"
csecret = "XXXX"
redirectURI = "http://localhost/"
username = "XXXX"


def startSpotify():
    app = Application(backend='win32').start(r'C:\Users\Maccrea P\AppData\Roaming\Spotify\Spotify.exe')
    dlg = app.window(title='Spotify Free')
    dlg_wrap = dlg.wrapper_object()
    dlg_wrap.wait_for_idle()
    return dlg_wrap


def playSpotify():
    spotify_win.send_keystrokes('{SPACE}')
    spotify_win.minimize()


def getToken():
    scope = 'user-read-playback-state'
    token = util.prompt_for_user_token(username, scope, cid, csecret, redirectURI)
    if token:
        auth_token = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    return auth_token


spotify_win = startSpotify()
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=csecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp = getToken()

while True:
    try:
        current_track = sp.current_playback()
        if current_track is not None:
            if current_track['currently_playing_type'] == 'ad':
                spotify_win.close()
                time.sleep(1)
                spotify_win = startSpotify()
                playSpotify()
            else:
                time.sleep(1)
        else:
            time.sleep(1)

    except spotipy.client.SpotifyException:
        sp = getToken()
