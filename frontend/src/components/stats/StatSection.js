import React, { Component } from "react";
import { render } from "react-dom";
import moment from 'moment';


import TrackTile from "../TrackTile.js";
import ArtistTile from "../ArtistTile.js";



class StatSection extends Component {
  constructor(props) {
    super(props);
  }

  albumCoverClick(track) {
    this.props.albumCoverClick(track);
  }

  render() {
    return (
      <div className="stats_section">
        <h3>{this.props.title}</h3>
        <div className="stats_artists">
          <div className="artists_top3">
            <div className="artist_rank1">
              {this.props.artists.slice(0, 1).map(
                (artist) =>
                  <ArtistTile artist={artist}
                    key={artist.id}
                    additionalInfo={
                      <>
                        #{artist.rank} • {artist.entry_count} listenings
                      </>
                    } />
              )}
            </div>
            <div className="artists_rank23">
              {this.props.artists.slice(1, 3).map(
                (artist) =>
                  <ArtistTile artist={artist}
                    key={artist.id}
                    additionalClassNames={`rank_${artist.rank}`}
                    additionalInfo={
                      <>
                        #{artist.rank} • {artist.entry_count} listenings
                      </>
                    } />
              )}
            </div>
          </div>
          <div className="artists_remaining">
            {this.props.artists.slice(3).map(
              (artist) =>
                <ArtistTile artist={artist}
                  key={artist.id}
                  additionalInfo={
                    <>
                      #{artist.rank} • {artist.entry_count} listenings
                    </>
                  } />
            )}
          </div>
        </div>

        <div className="stats_tracks">
          {this.props.tracks.map(
            (track) =>
              <TrackTile track={track}
                key={track.id}
                additionalClassNames={`rank_${track.rank}`}
                albumCoverClick={(track) => this.albumCoverClick(track)}
                clickable={true} showAlbum={false}
                additionalInfo={
                  <>
                    #{track.rank} • {track.entry_count} listenings
                  </>
                } />
          )}
        </div>
      </div>
    )
  }
}

export default StatSection;