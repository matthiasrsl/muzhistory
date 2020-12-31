import React, { Component } from "react";
import { render } from "react-dom";
import moment from 'moment';

import { IonApp, IonToggle, IonLabel } from "@ionic/react";
import {
  IonIcon,
} from '@ionic/react';
import { timeOutline, barChartOutline, hourglassOutline } from 'ionicons/icons';
import Player from "./Player.js";

import TrackTile from "./TrackTile.js";
import ListeningHistory from "./ListeningHistory.js";
import empty_track from "./empty_track.js";



import './App.css';

import { ThemeProvider } from "styled-components";
import { lightTheme, darkTheme } from "./themes.js";
import { GlobalStyles } from "./globalStyles.js";



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
            track_playing: profile.current_crush,
            theme: lightTheme
          };
        });
      });
  }


  albumCoverClick(track) {
    this.player.click(track);
  }

  toggleTheme(event) {
    this.setState({theme: event.detail.checked ? darkTheme : lightTheme });
  }

  render() {
    return (
      <ion-app>
        {this.state &&
          <ThemeProvider theme={this.state.theme}>
            <GlobalStyles />
            <div id="app_inner">
              <header>
                {this.state &&
                  <>
                    <div className="profile_infos">
                      <h1>{
                        this.state.profile.user.first_name ?
                          this.state.profile.user.first_name
                          : this.state.profile.user.username}
                      </h1>
                    </div>

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

                    <div className="config">
                      <IonLabel>Dark theme</IonLabel>
                      <IonToggle onIonChange={e => this.toggleTheme(e)}/>
                    </div>

                  </>
                }
              </header>

              <div className="main_content">
                <ListeningHistory albumCoverClick={
                  (track) => { this.albumCoverClick(track); }
                } />
              </div>
            </div>
            <Player track={this.state.profile.current_crush} 
              darkTheme={this.state.theme == darkTheme} ref={ref => this.player = ref} />
          </ThemeProvider>
        }
      </ion-app>
    )
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);