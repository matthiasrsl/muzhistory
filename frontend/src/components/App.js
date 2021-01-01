import React, { Component } from "react";
import { render } from "react-dom";

import { IonToggle, IonLabel } from "@ionic/react";
import {
  IonIcon,
} from '@ionic/react';
import {
  BrowserRouter as Router, Switch, Route, NavLink, Redirect
} from "react-router-dom";

import Player from "./Player.js";

import ListeningHistory from "./ListeningHistory.js";
import StatsPage from "./StatsPage.js"



import './App.css';

import { ThemeProvider } from "styled-components";
import { lightTheme, darkTheme } from "./themes.js";
import { GlobalStyles } from "./globalStyles.js";
var Tinycolor = require("tinycolor2");


var navlinks = [
  { label: "History", to: "/history" },
  { label: "Statistics", to: "/stats" },
  { label: "Year playlist", to: "/yearplaylist" },
  { label: "Profile", to: "/profile" }
]


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
            theme: darkTheme,
            palette: {
              background: "#222",
              text: "#fff",
              vibrant: "#fff"
            }
          };
        });
      });
  }


  albumCoverClick(track) {
    this.player.click(track);
  }

  toggleTheme(event) {
    this.setState({ theme: event.detail.checked ? darkTheme : lightTheme });
    this.updatePalette(this.state.vibrantPalette);
  }

  updatePalette(palette) {
    var workingPalette = {
      vibrant: palette.Vibrant.hex,
      lightVibrant: palette.LightVibrant.hex,
      darkVibrant: palette.DarkVibrant.hex,
      muted: palette.Muted.hex,
      lightMuted: Tinycolor(palette.LightMuted.hex).getBrightness() > 150 ?
        palette.LightMuted.hex :
        "#" + Tinycolor(
          palette.LightMuted.hex
        ).lighten(50).desaturate(60).toHex(),
      darkMuted: palette.DarkMuted.hex,
      softVibrant: "#" + Tinycolor(
        palette.Vibrant.hex
      ).desaturate(30).toHex()
    };

    var newPalette = {
      background: this.state.theme == lightTheme ? workingPalette.lightMuted : workingPalette.darkMuted,
      text: this.state.theme == lightTheme ? workingPalette.darkMuted : workingPalette.lightMuted,
      vibrant: workingPalette.vibrant,
      softVibrant: workingPalette.softVibrant
    }
    this.setState({ palette: newPalette, vibrantPalette: palette });
  }

  render() {
    return (
      <Router>
        {this.state &&
          <ThemeProvider theme={this.state.theme}>
            <GlobalStyles />
            <div id="app_inner">
              <header>
                {this.state &&
                  <>
                    <div className="color_tile" style={{
                      background: this.state.palette.background,
                    }}>

                    </div>
                    <div className="profile_infos">
                      <h1>{
                        this.state.profile.user.first_name ?
                          this.state.profile.user.first_name
                          : this.state.profile.user.username}
                      </h1>
                    </div>

                    <nav>
                      <ul>
                        {navlinks.map((page) =>
                          <li>
                            <NavLink key={page.id}
                              className="navbar_link"
                              activeClassName="navbar_link_active"
                              style={{
                                text: this.state.palette.text,
                                borderColor: this.state.palette.softVibrant
                              }}
                              activeStyle={{
                                background: this.state.palette.background,

                              }}
                              to={page.to}>
                              {page.label}
                            </NavLink>
                          </li>
                        )}
                      </ul>
                    </nav>

                    <div className="config">
                      <IonLabel>Dark theme</IonLabel>
                      <IonToggle checked={this.state.theme == darkTheme}
                        onIonChange={e => this.toggleTheme(e)} />
                    </div>

                  </>
                }
              </header>

              <div className="main_content">
                <Switch>
                  <Route path="/history">
                    <ListeningHistory albumCoverClick={
                      (track) => { this.albumCoverClick(track); }
                    } />
                  </Route>
                  <Route path="/stats">
                    <StatsPage albumCoverClick={
                      (track) => { this.albumCoverClick(track); }
                    } />
                  </Route>
                  <Route path="/">
                    <Redirect to="/history" />
                  </Route>
                </Switch>
              </div>
            </div>
            <Player track={this.state.profile.current_crush}
              darkTheme={this.state.theme == darkTheme}
              ref={ref => this.player = ref}
              updatePalette={(palette) => { this.updatePalette(palette) }}
              palette={this.state.palette}
            />
          </ThemeProvider>
        }
      </Router>
    )
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);