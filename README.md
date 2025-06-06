# Tunely AI Playlist Generator

## Overview
Tunely is an AI-powered playlist generator that creates personalized Spotify playlists based on user preferences. Using Gemini AI for intelligent song recommendations and Spotify's API for music integration, it transforms mood descriptions or themes into curated playlists. 
Here are the tech stack badges for Tunely AI Playlist in the same style

![React](https://img.shields.io/badge/Powered_By-React-blueviolet)
![Flask](https://img.shields.io/badge/Powered_By-Flask-orange)
![Gemini](https://img.shields.io/badge/API-Gemini-blue)
![Spotify](https://img.shields.io/badge/API-Spotify-green)

## Setup Instructions

### Prerequisites

- Python 3.8+ (for backend)
- Spotify Developer Account
- Google Cloud Account (for Gemini API)

### Clone the repository:

``` bash
git clone https://github.com/kapish19/tunely-ai-playlist.git
cd tunely-ai-playlist 
```

### Backend (Flask) Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
   GOOGLE_API_KEY=your_gemini_api_key
   
   ```

5. Run the Flask server:
   ```bash
   python app.py
   -- or 
   python3 app.py
   ```

### Frontend (React) Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file with:
   ```
   REACT_APP_REDIRECT_URI=http://localhost:5001
   ```

4. Start the React development server:
   ```bash
   npm start
   ```

## API Integration Details

### Spotify API Integration

## Core Implementation
- Uses Spotify OAuth 2.0 via `spotipy` library
- Requires `playlist-modify` scopes
- Key features:
  - Search tracks by title/artist
  - Create playlists programmatically
  - Automatic cleanup of old playlists

## Workflow
1. Gets AI-generated song recommendations
2. Searches Spotify for each track
3. Creates playlist with found tracks
4. Returns Spotify playlist URL to user

## Error Handling
- Fallback search when exact matches fail
- Validates minimum 15 tracks
- Graceful API error responses

## Requirements
- Spotify Developer account
- Valid client ID/secret
- Configured redirect URI

### Gemini AI Integration
The backend uses Gemini AI for:
- Analyzing user preferences
- Generating playlist themes and descriptions
- Recommending tracks based on mood/activity

## Development Workflow

1. Start both servers:
   ```bash
   # In backend directory
   python app.py
   
   # In frontend directory (new terminal)
   npm start
   ```

2. The application will be available at:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000


## Environment Variables Reference

### Backend (.env)
| Variable | Description |
|----------|-------------|
| SPOTIFY_CLIENT_ID | Spotify API client ID |
| SPOTIFY_CLIENT_SECRET | Spotify API client secret |
| SPOTIFY_REDIRECT_URI | Callback URL for Spotify auth |
| GEMINI_API_KEY | Google Gemini API key |

### Frontend (.env)
| Variable | Description |
|----------|-------------|
| REACT_APP_REDIRECT_URI | Frontend callback URL |

## Troubleshooting

1. **CORS Issues**: Ensure your Flask backend has CORS properly configured
2. **Spotify Auth Errors**: Verify redirect URIs match exactly in Spotify Developer Dashboard
3. **Gemini API Errors**: Check your Google Cloud project has Gemini API enabled
