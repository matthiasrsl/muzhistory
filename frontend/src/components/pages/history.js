import React, { Component } from 'react';

import TrackTile from "../TrackTile.js";
import Player from "../Player.js";

import "./track_snippet.css";
import "./HistoryPage.css";

var empty_track = {
  "id": 175,
  "track_type": "empty",
  "disc_number": null,
  "track_number": null,
  "duration": 600,
  "album_title": "Album title",
  "album_cover": "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/380x380-000000-80-0-0.jpg",
  "title": "Title ",
  "title_refine": "(Title refine)",
  "contributors": [
    {
      "name": "Main artist",
      "role": "main"
    },
    {
      "name": "Featured artist",
      "role": "feat"
    }
  ],
  "preview": ""
};

class HistoryPage extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    fetch("/api/history")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true,
            track_playing: empty_track
          };
        });
      });
  }

  changeTrack(track) {
    this.setState({track_playing: track});
    console.log(track)
  }

  render() {
    return (
      <>
        <div className="listening_history">
          {this.state && this.state.data.data.map((entry) =>
            <TrackTile track={entry.track} key={entry.id} 
                changeTrack={(track) => this.changeTrack(track)} 
            />
          )}
        </div>
        {this.state && <Player track={this.state.track_playing} />}
      </>
    )
  }
}





export default HistoryPage;
