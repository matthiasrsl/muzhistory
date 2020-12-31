import React, { Component } from 'react';

import './TrackTile.css'

class TrackTile extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="track" key={this.props.id}>
        <div className="album_cover" onClick={
          () => this.props.albumCoverClick(this.props.track)
        }>
          <img className={this.props.track.preview && "play_extract"}
            title={
              this.props.clickable &&
                this.props.track.preview ?
                "Play extract" : undefined
            }
            src={this.props.track.album_cover} alt="album"
          />
        </div>
        <div className="track_metadata">
          <p className="track_title">
            {this.props.track.title}
            <span className="track_title_refine">
              {this.props.track.title_refine}
            </span>
          </p>
          <p className="artists">
            {this.props.track.contributors.map((contrib, i, contribArray) =>
              <span
                className={`artist_name artist_name_role_${contrib.role} ${contrib.role == 'feat' ? 'muted_text' : ''}`}
                key={i}
              >
                {contrib.name}
                {i != contribArray.length - 1 && <span>, </span>}
              </span>
            )} {(this.props.showAlbum && this.props.track.album_title) && <> <span className="bullet">•</span> <span className="album_name">{
              this.props.track.album_title}
            </span> </>}
          </p>

          <p className="additional_info">{this.props.additionalInfo}</p>
        </div>
      </div>
    )
  }
}

export default TrackTile;