import React, { Component } from 'react';
import { IonIcon, IonRange } from '@ionic/react';

import { play, pause, volumeMedium } from 'ionicons/icons';


import TrackTile from "./TrackTile.js";

import "./Player.css";

var Tinycolor = require("tinycolor2");
var Vibrant = require("node-vibrant");
var ProgressBar = require("progressbar.js");



function formatDuration(duration) {
  return new Date(duration * 1000).toISOString().substr(14, 5);
}


class Player extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      track: this.props.track, 
      position: 0, 
      loaded: false,
      palette: {
        vibrant: "#000",
        lightVibrant: "#000",
        darkVibrant: "#000",
        muted: "#000",
        lightMuted: "#000",
        darkMuted: "#000"
      }
    };
  }

  componentDidMount() {
    this.changeTrack(this.props.track, false);
    this.audio.volume = 0.5;
  }

  click(track) {
    this.changeTrack(track);
    this.playPause();
  }

  createProgressBar() {
    var progress_container = this.progress_container;
    if (this.progressBar) {
      this.progressBar.destroy();
    }
    var bar = new ProgressBar.Line(progress_container, {
      strokeWidth: 6,
      easing: 'easeInOut',
      duration: 1,
      color: this.state.palette.vibrant,
      trailColor: this.state.palette.lightMuted,
      trailWidth: 1,
      svgStyle: { width: '100%', height: '100%' }
    });
    this.progressBar = bar;



    this.updateProgressBar();
  }

  getPalette(track) {
    var vibrant = Vibrant.from(track.album_cover);
    vibrant.getPalette((err, palette) => {
      this.setState({
        palette: {
          vibrant: palette.Vibrant.hex,
          lightVibrant: palette.LightVibrant.hex,
          darkVibrant: palette.DarkVibrant.hex,
          muted: palette.Muted.hex,
          lightMuted: palette.LightMuted.hex,
          darkMuted: palette.DarkMuted.hex
        }
      }, this.createProgressBar);
    })
  }

  initProgressBar(track) {
    this.getPalette(track);
  }

  changeTrack(track, play = true) {
    var audio = this.audio; this.setState((prevState, props) => ({ track: track }));
    this.setState((prevState, props) => ({ track: track }));
    if (audio.src != track.preview) {
      this.setState({ loaded: false });
      audio.src = track.preview;
      audio.load();
      audio.oncanplay = (event) => { this.audioLoaded(play); }
      audio.ontimeupdate = (event) => { this.updateProgressBar(event); }
      this.initProgressBar(track);
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

  audioLoaded(play = true) {
    if (play) {
      this.audio.play();
      this.setState({ playing: true });
    }
    this.totalTimeElement.firstChild.replaceWith(
      formatDuration(this.state.track.duration)
    );
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
    this.progressBar.set(current_time / duration);

  }

  changeVolume(e) {
    var audio = this.audio;
    audio.volume = e.detail.value / 100;
  }

  render() {
    return (
      <div className="player" style={{ background: this.state.palette.darkMuted}}>
        <audio id="player_audio" src="" data-currently-playing-id=""
          data-begin-time="30" ref={ref => this.audio = ref}>
        </audio>

        <TrackTile track={this.state.track} coverClick={(track) => { }}
          clickable={false} showAlbum={false}
        />

        <div className="player_time_infos">
          {this.state.playing ?
            <IonIcon className="playpause-icon pause" icon={pause} onClick={
              () => this.playPause()
            } />
            : <IonIcon className="playpause-icon play" icon={play} onClick={
              () => this.playPause()
            } />
          }

          <div className="player_progress">
            <p id="player_current_time"
              ref={ref => this.currentTimeElement = ref}
            >0:00</p>
            <div className="progress_container" ref={
              ref => this.progress_container = ref
            }>
            </div>
            <p id="player_total_time"
              ref={ref => this.totalTimeElement = ref}
            > 0:00</p>
          </div>
        </div>

        <div className="player_options">
          <IonIcon icon={volumeMedium} />
          <div className="volume_slider">
            <IonRange value={50} onIonChange={e => this.changeVolume(e)} 
              ref={ref => this.volumeSlider = ref}/>
          </div>

        </div>

      </div >
    )
  }
}

export default Player;