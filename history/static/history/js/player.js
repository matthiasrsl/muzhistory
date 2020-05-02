function initPlayer() {
    var player_album_cover = document.querySelector(
        ".player .album_cover"
    );
    player_album_cover.onclick = "";
    player_album_cover.firstElementChild.title = "";
}


function play(id) {
    var album_cover_url = document.querySelector("#track_" + id + " img").src;
    var track_metadata = document.querySelector(
        "#track_" + id + " .track_metadata"
    ).cloneNode(true);
    /* var track_title_short = document.querySelector(
        "#track" + id + " .track_title"
    ).firstChild;
    var track_title_short = document.querySelector(
        "#track" + id + " .track_title_version"
    ).firstChild;
    var artists = document.querySelector("#track" + id + " .artists").src;
    var */
    var player_album_cover = document.querySelector(
        ".player .album_cover img"
    );
    var player_track_metadata = document.querySelector(
        ".player .track_metadata"
    );
    player_album_cover.src = album_cover_url;
    player_track_metadata.replaceWith(track_metadata);
    var album_name = document.querySelector(".player .album_name");
    if (album_name != null) {
        document.querySelector(".player .additional_info").remove();
    }

    var allaudios = document.querySelectorAll('audio');
    var audio = document.getElementById("audio_" + id);
    if (audio.paused) {
        for (var i = 0; i < allaudios.length; i++) {
            allaudios[i].pause();
        }
        audio.play();
    } else {
        audio.pause();
    }
}

initPlayer();