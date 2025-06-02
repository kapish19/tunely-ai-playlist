import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

function App() {
    const [info, setInfo] = useState("");
    const [playlistUrl, setPlaylistUrl] = useState("");
    const [loading, setLoading] = useState(false);

    const generatePlaylist = async () => {
        setLoading(true);
        setPlaylistUrl("");

        try {
            const response = await axios.post("http://localhost:5001/generate_playlist", { info });
            setPlaylistUrl(response.data.playlist_url);
        } catch (error) {
            console.error("Error generating playlist:", error);
        } finally {
            setTimeout(() => setLoading(false), 1200); // Smooth delay effect
        }
    };

    return (
        <div className="container">
            <div className="window">
                <div className="title-bar">Tunely : Generate Your Customized Playlist</div>

                <div className="content">
                    <p className="instruction">
                        Tell us what you're feeling, what you love, or the kind of songs you want, 
                        and we'll create a personalized playlist just for you!
                    </p>

                    <input
                        type="text"
                        placeholder="Type here..."
                        value={info}
                        onChange={(e) => setInfo(e.target.value)}
                        className="input-box"
                    />

                    <button onClick={generatePlaylist} className="btn" disabled={loading}>
                        {loading ? (
                            <>
                                Loading...
                                <span className="loading-spinner"></span>
                            </>
                        ) : (
                            "Generate Playlist"
                        )}
                    </button>

                    {playlistUrl && (
                        <div className="playlist-box">
                            <p>Your Playlist:</p>
                            <a href={playlistUrl} target="_blank" rel="noopener noreferrer">Open Playlist</a>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default App;
