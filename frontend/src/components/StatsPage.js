import React, { Component } from "react";
import { render } from "react-dom";

import StatSection from "./stats/StatSection.js"

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
              <StatSection title="Past 7 days"
                key={1}
                artists={this.state.data.artists_7_days}
                tracks={this.state.data.tracks_7_days}
                albumCoverClick={(track) => this.albumCoverClick(track)} />

              <StatSection title="Past 30 days"
                key={2}
                artists={this.state.data.artists_30_days}
                tracks={this.state.data.tracks_30_days}
                albumCoverClick={(track) => this.albumCoverClick(track)} />

              <StatSection title="This year"
                key={3}
                artists={this.state.data.artists_this_year}
                tracks={this.state.data.tracks_this_year}
                albumCoverClick={(track) => this.albumCoverClick(track)} />

              <StatSection title="All time"
                key={4}
                artists={this.state.data.artists_all_time}
                tracks={this.state.data.tracks_all_time}
                albumCoverClick={(track) => this.albumCoverClick(track)} />
            </div>
          </div>
        }
      </>
    )
  }
}

export default StatsPage;