import React, { Component } from 'react';

import TrackTile from "./TrackTile.js";

import "./Player.css";

var Tinycolor = require("tinycolor2");
var Vibrant = require("node-vibrant");
var Progressbar = require("progressbar.js");



class Player extends Component {
  constructor(props) {
    super(props);
    this.state = { track: this.props.track, position: 0 };
  }

  play() {
    var audio = this.audio;
    audio.play();
    console.log("Playing !");
  }

  componentDidUpdate() {
    this.play();
  }

  render() {
    return (
      <div className="player">
        <TrackTile track={this.props.track} />
        <div className="player_time_infos">
          <div className="progress_container"></div>
          <div>
            <p className="player_label">30 secondes d'extrait</p>
            <p className="player_time">
              <span id="player_current_time">0:00</span> /
              <span id="player_total_time">0:00</span>
            </p>
          </div>
        </div>
        <audio id="player_audio" src={this.props.track.preview} data-currently-playing-id="" data-begin-time="" ref={ref => this.audio = ref}>
        </audio>
      </div>
    )
  }
}

export default Player;