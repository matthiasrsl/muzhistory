import React, { Component } from 'react';
import { IonIcon, IonProgressBar } from '@ionic/react';

import { play, pause } from 'ionicons/icons';

import TrackTile from "./TrackTile.js";

import "./Player.css";

var Tinycolor = require("tinycolor2");
var Vibrant = require("node-vibrant");

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
  "preview": "https://cdns-preview-7.dzcdn.net/stream/c-79a4f779d296204d674a37c8eb002978-5.mp3"
};


function formatDuration(duration) {
  return new Date(duration * 1000).toISOString().substr(14, 5);
}


class Player extends Component {
  constructor(props) {
    super(props);
    this.state = { track: this.props.track, position: 0, loaded: false };
  }

  componentDidMount() {
    this.changeTrack(this.props.track, false);
  }

  click(track) {
    this.setState((prevState, props) => ({ track: track }));
    this.changeTrack(track);
    this.playPause();
    this.show();
  }

  changeTrack(track, play = true) {
    var audio = this.audio;
    if (audio.src != track.preview) {
      this.setState({ loaded: false });
      audio.src = track.preview;
      audio.load();
      this.progressBar.value = (
        this.audio.dataset.beginTime / this.state.track.duration
      );
      audio.oncanplay = (event) => { this.audioLoaded(play); }
      audio.ontimeupdate = (event) => { this.updateProgressBar(event); }
      audio.onended = (event) => { this.hide(); };
    }
  }

  playPause() {
    var audio = this.audio;
    if (audio.paused) {
      audio.play();
      this.setState({ playing: true });
    } else {
      if (this.state.loaded) {
        audio.pause();
        this.setState({ playing: false });
      }
    }
  }

  show() {
    var playerElement = document.querySelector(".player");
    playerElement.style.bottom = "0";
  }

  hide() {
    var playerElement = document.querySelector(".player");
    playerElement.style.bottom = "-200px";
  }

  audioLoaded(play = true) {
    if (play) {
      this.audio.play();
      this.setState({ playing: true });
      this.progressBar.type = "determinate";
      this.totalTimeElement.firstChild.replaceWith(
        formatDuration(this.state.track.duration)
      );
    }
    this.setState({ loaded: true });
  }

  updateProgressBar(event) {
    var begin_time = this.audio.dataset.beginTime;
    var duration = this.state.track.duration;
    var current_time = parseInt(begin_time) + parseFloat(
      this.audio.currentTime
    );
    this.currentTimeElement.firstChild.replaceWith(
      formatDuration(current_time)
    );
    this.progressBar.value = (current_time / duration);
  }

  render() {
    return (
      <div className="player">
        <audio id="player_audio" src="" data-currently-playing-id=""
          data-begin-time="30" ref={ref => this.audio = ref}>
        </audio>
        <TrackTile track={this.state.track} coverClick={(track) => { }}
          clickable={false}
          additionalInfo={
            this.state.loaded ?
              this.state.playing ? "Now playing" : "Paused"
              : "Loading..."
          }
        />
        <div className="player_time_infos">
          <div className="progress_container">
            <IonProgressBar color="primary"
              ref={ref => this.progressBar = ref}>
            </IonProgressBar>
          </div>
          <div>
            <p className="player_label">30-second extract</p>
            <p className="player_time">
              <span id="player_current_time"
                ref={ref => this.currentTimeElement = ref}
              >0:00</span> / <span id="player_total_time"
                ref={ref => this.totalTimeElement = ref}
              > 0:00</span>
            </p>
          </div>
          {this.state.playing ?
            <IonIcon className="playpause-icon" icon={pause} onClick={
              () => this.playPause()
            } />
            : <IonIcon className="playpause-icon" icon={play} onClick={
              () => this.playPause()
            } />
          }
        </div>
      </div>
    )
  }
}

export default Player;