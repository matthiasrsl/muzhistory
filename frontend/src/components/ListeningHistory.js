import React, { Component } from "react";
import { render } from "react-dom";
import moment from 'moment';

import {
  IonIcon,
} from '@ionic/react';
import { timeOutline } from 'ionicons/icons';

import TrackTile from "./TrackTile.js";
import empty_track from "./empty_track.js";


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
          <>
            <h2>Your listening history</h2>
            <div className="listening_history">
              {this.state.data.data.map((entry) =>
                <TrackTile track={entry.track} key={entry.id}
                  albumCoverClick={(track) => this.albumCoverClick(track)}
                  clickable={true} showAlbum={true}
                  additionalInfo={
                    <>
                      <IonIcon icon={timeOutline} />
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
          </>
        }
      </>
    )
  }
}

export default ListeningHistory;