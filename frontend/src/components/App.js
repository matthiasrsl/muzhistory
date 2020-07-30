import React, { Component } from "react";
import { render } from "react-dom";
import { Redirect, Route } from 'react-router-dom';

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
import {timeOutline, barChartOutline} from 'ionicons/icons';
import HistoryPage from './pages/history';
import StatsPage from './pages/stats';

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';



class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  /*componentDidMount() {
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
            loaded: true
          };
        });
      });
  }*/

  render() {
    return (
    <IonReactRouter>
      <IonTabs>
        <IonRouterOutlet>
          <Route path="/history" component={HistoryPage} exact={true} />
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
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);