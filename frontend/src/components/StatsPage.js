import React, { Component } from "react";
import { render } from "react-dom";
import moment from 'moment';

import {
  IonIcon,
} from '@ionic/react';
import { timeOutline, barChartOutline, hourglassOutline, listOutline } from 'ionicons/icons';

import TrackTile from "./TrackTile.js";
import empty_track from "./empty_track.js";

import './ListeningHistory.css';


class StatsPage extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
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
            loaded: true,
          };
        });
      });
  }

  albumCoverClick(track) {
    this.props.albumCoverClick(track);
  }

  render() {
    return (
      <>
        {
          this.state &&
          <div className="stats_page">
            <div className="page_header">
              <h2>Your statistics</h2>
            </div>
          </div>
        }
      </>
    )
  }
}

export default StatsPage;