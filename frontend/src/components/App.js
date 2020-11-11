import React, { Component } from "react";
import { render } from "react-dom";
import moment from 'moment';

import { IonApp } from "@ionic/react";
import {
  IonIcon,
} from '@ionic/react';
import { timeOutline, barChartOutline, hourglassOutline } from 'ionicons/icons';
import Player from "./Player.js";

import TrackTile from "./TrackTile.js";
import ListeningHistory from "./ListeningHistory.js";
import empty_track from "./empty_track.js";



import './App.css';



class App extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    fetch("/api/profile")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(profile => {
        this.setState(() => {
          return {
            profile,
            loaded: true,
            track_playing: empty_track
          };
        });
      });
  }


  albumCoverClick(track) {
    this.player.click(track);
  }

  render() {
    return (
      <ion-app>
        <div id="app_inner">
          <header>
            <div className="inner_header">
              {this.state &&
                <>
                  <div className="profile_infos">
                    <h1>{
                      this.state.profile.user.first_name ?
                        this.state.profile.user.first_name
                        : this.state.profile.user.username
                    }'s listening history
                  </h1>
                  </div>
                  <div className="lower_header">
                    <div className="history_metadata">
                      <p title="Number of listenings">
                        {this.state.profile.nb_listenings} listenings
                    </p>
                      <p title="Total listening time">
                        <IonIcon icon={hourglassOutline} />
                        {Math.floor(this.state.profile.listening_duration / 3600)} hours
                    </p>
                      <p title="Last update">
                        <IonIcon icon={timeOutline} />
                        {moment(this.state.profile.last_update).calendar(
                          null,
                          { sameElse: "LL" }
                        ).toLowerCase()}
                      </p>
                    </div>
                    {this.state.profile.current_crush ?
                      <aside className="current_crush">
                        <TrackTile track={this.state.profile.current_crush}
                          albumCoverClick={(track) => this.albumCoverClick(track)}
                          additionalInfo="Your current crush" />
                      </aside> : undefined
                    }
                  </div>
                </>
              }
            </div>
          </header>
          <div className="main_content">
            <ListeningHistory albumCoverClick={
              (track) => { this.albumCoverClick(track); }
            } />
          </div>
        </div>
          <Player ref={ref => this.player = ref} />
      </ion-app>
    )
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);