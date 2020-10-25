import React, { Component } from 'react';
import { IonProgressBar } from '@ionic/react';

import TrackTile from "./TrackTile.js";

import "./Player.css";

var Tinycolor = require("tinycolor2");
var Vibrant = require("node-vibrant");
var Progressbar = require("progressbar.js");

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
    this.state = { track: empty_track, position: 0 };
  }

  click(track) {
    this.setState((prevState, props) => ({ track: track }));
    this.playPause(track);
    this.show();
  }

  playPause(track) {
    var audio = this.audio;
    if (audio.src != track.preview) {
      audio.src = track.preview;
      audio.load();
      this.progressBar.value = (
        this.audio.dataset.beginTime / this.state.track.duration
      );
      audio.oncanplay = (event) => { this.audioLoaded(); }
      audio.ontimeupdate = (event) => { this.updateProgressBar(event); }
      audio.onended = (event) => { this.hide(); };
    } else {
      if (audio.paused) {
        audio.play();
      } else {
        audio.pause();
      }
    }
  }

  show() {
    var playerElement = document.querySelector(".player");
    playerElement.style.bottom = "0";
    this.totalTimeElement.firstChild.replaceWith(
      formatDuration(this.state.track.duration)
    );
  }

  hide() {
    var playerElement = document.querySelector(".player");
    playerElement.style.bottom = "-200px";
  }

  audioLoaded() {
    this.audio.play();
    this.progressBar.type = "determinate";
  }

  updateProgressBar(event) {
    var begin_time = this.audio.dataset.beginTime;
    var duration = this.state.track.duration;
    var current_time = parseInt(begin_time) + parseFloat(this.audio.currentTime);
    this.currentTimeElement.firstChild.replaceWith(
      formatDuration(current_time)
    );
    this.progressBar.value = (current_time / duration);
  }

  render() {
    return (
      <div className="player">
        <TrackTile track={this.state.track} coverClick={(track) => {}}/>
        <div className="player_time_infos">
          <div className="progress_container">
            <IonProgressBar color="primary" ref={ref => this.progressBar = ref}>
            </IonProgressBar>
          </div>
          <div>
            <p className="player_label">30 secondes d'extrait</p>
            <p className="player_time">
              <span id="player_current_time"
                ref={ref => this.currentTimeElement = ref}
              >0:00</span> / <span id="player_total_time"
                ref={ref => this.totalTimeElement = ref}
              > 0:00</span>
            </p>
          </div>
        </div>
        <audio id="player_audio" src="#" data-currently-playing-id="" data-begin-time="30" ref={ref => this.audio = ref}>
        </audio>
      </div>
    )
  }
}

export default Player;