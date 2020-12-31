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


class ListeningHistory extends Component {
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
            track_playing: empty_track
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
          <div className="history_page">
            <div className="page_header">
              <h2>Your listening history</h2>

              <div className="history_metadata">
                <p title="Number of listenings">
                  <IonIcon icon={listOutline} />
                  {this.state.data.profile.nb_listenings} listenings
                    </p>
                <p title="Total listening time">
                  <IonIcon icon={hourglassOutline} />
                  {Math.floor(this.state.data.profile.listening_duration / 3600)} hours
                    </p>
                <p title="Last update">
                  <IonIcon icon={timeOutline} />
                  {moment(this.state.data.profile.last_update).calendar(
                    null,
                    { sameElse: "LL" }
                  ).toLowerCase()}
                </p>
              </div>
            </div>
            <div className="listening_history">
              {this.state.data.data.map((entry) =>
                <TrackTile track={entry.track} key={entry.id}
                  albumCoverClick={(track) => this.albumCoverClick(track)}
                  clickable={true} showAlbum={true}
                  additionalInfo={
                    <>
                      <IonIcon icon={timeOutline} title="Listened on" />
                      <span>
                        {moment(entry.listening_datetime).calendar(
                          null,
                          { sameElse: "LL" }
                        ).toLowerCase()}
                      </span>
                    </>
                  }
                />
              )}
            </div>
          </div>
        }
      </>
    )
  }
}

export default ListeningHistory;