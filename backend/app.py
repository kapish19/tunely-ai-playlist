from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import threading
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# ✅ Configure Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:5001/callback"),
    scope="playlist-modify-public playlist-modify-private"
))

# Manage playlist expiration
playlists = {}
playlist_lock = threading.Lock()

def cleanup_playlists():
    while True:
        time.sleep(3600)  # Every 1 hour
        current_time = time.time()
        with playlist_lock:
            expired_playlists = [
                playlist_id for playlist_id, created_time in playlists.items()
                if current_time - created_time > 3600
            ]
            for playlist_id in expired_playlists:
                try:
                    sp.user_playlist_unfollow(sp.current_user()['id'], playlist_id)
                    del playlists[playlist_id]
                except Exception as e:
                    print(f"Error deleting playlist {playlist_id}: {e}")

cleanup_thread = threading.Thread(target=cleanup_playlists, daemon=True)
cleanup_thread.start()

# API to generate a playlist
@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    data = request.json
    user_prompt = data.get("info", "")

    if not user_prompt:
        return jsonify({"error": "Please provide input"}), 400

    try:
        # Gemini AI prompt for at least 15-20 songs
        prompt = f"""
        You are a music recommendation expert. Based on the user's mood: "{user_prompt}", 
        generate **at least 15-20 song recommendations**.
        Respond **only** in this format:
        1. Song Name - Artist Name
        2. Song Name - Artist Name
        3. Song Name - Artist Name
        ...
        Up to 20 songs in total. No extra text.
        """

        response = model.generate_content(prompt)
        raw_songs = response.text.strip().split("\n")

        # Extract valid songs using regex
        songs = []
        for song in raw_songs:
            match = re.match(r"^\d+\.\s(.+?)\s-\s(.+)$", song)  # Matches "1. Song - Artist"
            if match:
                songs.append(f"{match.group(1)} - {match.group(2)}")

        if len(songs) < 15:
            return jsonify({"error": "Gemini AI did not return enough valid songs"}), 500

        # Generate a Meaningful Playlist Name
        playlist_name_prompt = f"""
        Based on this mood or theme: "{user_prompt}", suggest a **creative and engaging playlist name**.
        Respond **only** with the playlist name, no extra text.
        """
        playlist_response = model.generate_content(playlist_name_prompt)
        playlist_name = playlist_response.text.strip()

        # Fetch songs from Spotify
        song_uris = fetch_songs_from_spotify(songs)

        if len(song_uris) < 15:
            return jsonify({"error": "Not enough songs found on Spotify"}), 500

        # Create a Spotify playlist with the generated name
        user_id = sp.current_user()["id"]
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        sp.playlist_add_items(playlist["id"], song_uris)

        return jsonify({
            "playlist_name": playlist_name,
            "playlist_url": playlist["external_urls"]["spotify"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def fetch_songs_from_spotify(songs):
    song_uris = []
    missing_songs = []

    for song in songs:
        try:
            title, artist = song.split(" - ")
            query = f"track:{title} artist:{artist}"
            result = sp.search(q=query, limit=1, type='track')

            if result["tracks"]["items"]:
                song_uris.append(result["tracks"]["items"][0]["uri"])
            else:
                print(f"❌ No result found for: {song}")
                missing_songs.append(song)

        except Exception as e:
            print(f"⚠️ Error searching for {song}: {e}")

    # ✅ If missing songs exist, retry with only the title
    if missing_songs:
        print("🔄 Retrying search with song titles only...")
        for song in missing_songs:
            try:
                title = song.split(" - ")[0]
                result = sp.search(q=f"track:{title}", limit=1, type='track')

                if result["tracks"]["items"]:
                    song_uris.append(result["tracks"]["items"][0]["uri"])
            except Exception as e:
                print(f"⚠️ Error retrying search for {song}: {e}")

    return song_uris

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "AI Playlist Generator Backend is Running!"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
