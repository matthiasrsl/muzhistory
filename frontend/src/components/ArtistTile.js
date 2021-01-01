import React, { Component } from 'react';

import './ArtistTile.css'

class ArtistTile extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="artist"
        key={this.props.id}>
        <div className="image">
          <img className="artist_image"
            src={this.props.artist.image} alt={this.props.artist.name}
          />
        </div>
        <div className="artist_info">
          <p className="artist_name">
            {this.props.artist.name}
          </p>

          <p className="additional_info">{this.props.additionalInfo}</p>
        </div>
      </div>
    )
  }
}

export default ArtistTile;