import React, { Component } from "react";
import { render } from "react-dom";
import moment from 'moment';

import {
  IonIcon,
} from '@ionic/react';
import { timeOutline, barChartOutline, hourglassOutline, listOutline } from 'ionicons/icons';

import TrackTile from "./TrackTile.js";
import empty_track from "./empty_track.js";

import './StatsPage.css';


class StatsPage extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    fetch("/api/stats")
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

            <div className="page_content">
              <div className="stats_section stats_all_time">
                <h3>All time</h3>
                {this.state.data.tracks_all_time.map(
                  (track) =>
                    <TrackTile track={track} key={track.rank}
                      albumCoverClick={(track) => this.albumCoverClick(track)}
                      clickable={true} showAlbum={false}
                      additionalInfo={track.entry_count + " listenings"} />
                )}
              </div>
            </div>
          </div>
        }
      </>
    )
  }
}

export default StatsPage;