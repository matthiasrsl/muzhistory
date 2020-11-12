import { IonIcon } from '@ionic/react';
import React, { Component } from 'react';
import moment from 'moment';

import TrackTile from "../TrackTile.js";

import "./HistoryPage.css";

import { timeOutline, hourglassOutline } from 'ionicons/icons';

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

class HistoryPage extends Component {
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
    this.setState({ track_playing: track });
  }

  render() {
    return (
      <>
        <header>
          <div className="inner_header">
            {this.state &&
              <>
                <div className="profile_infos">
                  <h1>{
                    this.state.data.profile.user.first_name ?
                      this.state.data.profile.user.first_name
                      : this.state.data.profile.user.username
                  }'s listening history
                  </h1>
                </div>
                <div className="lower_header">
                  <div className="history_metadata">
                    <a className="stats_link" href="/oldhistory/stats/">Statistics</a>
                    <p title="Number of listenings">
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
                  {this.state.data.profile.current_crush ?
                    <aside className="current_crush">
                      <TrackTile track={this.state.data.profile.current_crush}
                        albumCoverClick={(track) => this.albumCoverClick(track)}
                        additionalInfo="Your current crush" />
                    </aside> : undefined
                  }
                </div>
              </>
            }
          </div>
        </header>
        {this.state &&
          <>
            <section>
              <div className="listening_history">
                {this.state.data.data.map((entry) =>
                  <TrackTile track={entry.track} key={entry.id}
                    albumCoverClick={(track) => this.albumCoverClick(track)}
                    clickable={true}
                    additionalInfo={
                      <>
                        <IonIcon icon={timeOutline} />
                        <span>
                          Listened to {moment(entry.listening_datetime).calendar(
                          null,
                          { sameElse: "[on] LL" }
                        ).toLowerCase()}
                        </span>
                      </>
                    }
                  />
                )}
              </div>
            </section>
          </>
        }
      </>
    )
  }
}





export default HistoryPage;
