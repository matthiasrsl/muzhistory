import React, { Component } from "react";
import { render } from "react-dom";
import { Redirect, Route } from 'react-router-dom';
import moment from 'moment';

import {
  IonApp,
  IonIcon,
  IonLabel,
  IonRouterOutlet,
  IonTabBar,
  IonTabButton,
  IonTabs
} from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { timeOutline, barChartOutline } from 'ionicons/icons';
import HistoryPage from './pages/HistoryPage';
import StatsPage from './pages/StatsPage';
import Player from "./Player.js";

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

import './App.css';

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

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    this.setState({
      track_playing: empty_track
    })
    moment.locale("fr");
  }

  albumCoverClick(track) {
    this.player.click(track);
  }

  render() {
    return (
      <>
        <IonReactRouter>
          <IonTabs>
            <IonRouterOutlet>
              <Route path="/history" component={
                () => <HistoryPage albumCoverClick={
                  (track) => { this.albumCoverClick(track); }
                } />
              } exact={true} />
              <Route path="/stats" component={StatsPage} exact={true} />
              <Route path="/" render={() => <Redirect to="/history" />} exact={true} />
            </IonRouterOutlet>
            <IonTabBar slot="top">
              <IonTabButton layout="icon-start" tab="history" href="/history">
                <IonIcon icon={timeOutline} />
                <IonLabel>History</IonLabel>
              </IonTabButton>
              <IonTabButton layout="icon-start" tab="stats" href="/stats">
                <IonIcon icon={barChartOutline} />
                <IonLabel>Statistics</IonLabel>
              </IonTabButton>
            </IonTabBar>
          </IonTabs>
        </IonReactRouter>
        <Player ref={ref => this.player = ref} />
      </>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);