import React, { Component } from 'react';
import { IonProgressBar } from '@ionic/react';

import TrackTile from "./TrackTile.js";

import "./Player.css";

var Tinycolor = require("tinycolor2");
var Vibrant = require("node-vibrant");
var Progressbar = require("progressbar.js");


function formatDuration(duration) {
  return new Date(duration * 1000).toISOString().substr(14, 5);
}


class Player extends Component {
  constructor(props) {
    super(props);
    this.state = { track: this.props.track, position: 0 };
  }

  play() {
    var audio = this.audio;
    audio.play();
    console.log("Playing !");
    this.progressBar.type = "indeterminate";
    this.progressBar.value = (
      this.audio.dataset.beginTime / this.props.track.duration
    );
    audio.oncanplay = (event) => { this.audioLoaded(); }
    audio.ontimeupdate = (event) => { this.updateProgressBar(event); }
    audio.onended = (event) => { this.hide(); };
  }

  show() {
    var playerElement = document.querySelector(".player");
    playerElement.style.bottom = "0";
    this.totalTimeElement.firstChild.replaceWith(
      formatDuration(this.props.track.duration)
    );
  }

  hide() {
    var playerElement = document.querySelector(".player");
    playerElement.style.bottom = "-200px";
  }

  audioLoaded() {
    this.progressBar.type = "determinate";
  }

  updateProgressBar(event) {
    var begin_time = this.audio.dataset.beginTime;
    var duration = this.props.track.duration;
    var current_time = parseInt(begin_time) + parseFloat(this.audio.currentTime);
    this.currentTimeElement.firstChild.replaceWith(
      formatDuration(current_time)
    );
    this.progressBar.value = (current_time / duration);
    /*if (this.audio.readyState >= 1) {
      /*this.progressBar.type = "determinate";
      this.progressBar.buffer = 1;
    } else {
      this.progressBar.buffer = (current_time / duration);
    }*/
  }

  componentDidUpdate() {
    if (this.props.track.preview) {
      this.play();
      this.show();
    } else {
      this.hide();
    }
  }

  render() {
    return (
      <div className="player">
        <TrackTile track={this.props.track} />
        <div className="player_time_infos">
          <div className="progress_container">
            <IonProgressBar color="primary" value={0.5} ref={ref => this.progressBar = ref}>
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
        <audio id="player_audio" src={this.props.track.preview} data-currently-playing-id="" data-begin-time="30" ref={ref => this.audio = ref}>
        </audio>
      </div>
    )
  }
}

export default Player;