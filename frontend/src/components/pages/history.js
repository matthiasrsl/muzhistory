import React, { Component } from 'react';



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
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <div>
        {this.state && this.state.data.data.map((entry) =>
          <img src={entry.track.album_cover} alt="album" key={entry.id} />
        )}
      </div>
    )
  }
}





export default HistoryPage;
