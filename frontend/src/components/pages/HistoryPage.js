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
        {this.state &&
          <>
            <header>
              <div className="inner_header">
                <div className="profile_infos">
                  <h1>Historique de {this.state.data.profile.user.username}</h1>
                  <p title="Nombre total d'écoutes">
                    {this.state.data.profile.nb_listenings} écoutes
                </p>
                  <p title="Durée totale d'écoute">
                    <IonIcon icon={hourglassOutline} />
                    {moment.duration(
                      this.state.data.profile.listening_duration, 'seconds'
                    ).hours()} heures
                </p>
                  <p title="Dernière mise à jour">
                    <IonIcon icon={timeOutline} />
                    {moment(this.state.data.profile.last_update).calendar(
                      null,
                      { sameElse: "[le] LL" }
                    ).toLowerCase()}
                  </p>
                </div>
                {this.state.data.profile.current_crush &&
                  <aside className="current_crush">
                    <TrackTile track={this.state.data.profile.current_crush}
                      albumCoverClick={(track) => this.albumCoverClick(track)}
                      additionalInfo="Votre titre du moment" />
                  </aside>
                }
              </div>
            </header>
            <section>
              <div className="listening_history">
                {this.state.data.data.map((entry) =>
                  <TrackTile track={entry.track} key={entry.id}
                    albumCoverClick={(track) => this.albumCoverClick(track)}
                    additionalInfo={
                      <>
                        <IonIcon icon={timeOutline} />
                        <span>
                          Écouté {moment(entry.listening_datetime).calendar(
                          null,
                          { sameElse: "[le] LL" }
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
