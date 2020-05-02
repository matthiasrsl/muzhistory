function initPlayer() {
    var player_album_cover = document.querySelector(
        ".player .album_cover"
    );
    player_album_cover.onclick = "";
    player_album_cover.firstElementChild.title = "";
}


function formatDuration(duration) {
    return new Date(duration * 1000).toISOString().substr(14, 5);
}

function showPlayer() {
    player = document.querySelector(".player");
    player.style.bottom = "0";
}

function hidePlayer(event) {
    player = document.querySelector(".player");
    player.style.bottom = "-200px";
}

function play(id) {
    showPlayer();
    var audio = document.querySelector("audio.player_audio");
    if (audio.dataset.currentlyPlayingId == id) {
        if (audio.paused) {
            audio.play();
        } else {
            audio.pause()
        }
    } else {
        var album_cover_url = document.querySelector("#track_" + id + " img").src;
        var track_metadata = document.querySelector(
            "#track_" + id + " .track_metadata"
        ).cloneNode(true);
        var duration = document.querySelector("#track_" + id).dataset.duration;
        var audioSrc = document.querySelector("#track_" + id).dataset.audioSrc;

        var player_album_cover = document.querySelector(
            ".player .album_cover img"
        );
        var player_track_metadata = document.querySelector(
            ".player .track_metadata"
        );
        var player_progress = document.querySelector(
            ".player progress"
        )
        var total_duration_element = document.querySelector(
            ".player #player_total_time"
        ).firstChild;
        var current_position_element = document.querySelector(
            ".player #player_current_time"
        ).firstChild;

        player_album_cover.src = album_cover_url;
        player_track_metadata.replaceWith(track_metadata);
        var album_name = document.querySelector(".player .album_name");
        if (album_name != null) {
            document.querySelector(".player .additional_info").remove();
        }
        player_progress.max = duration;
        total_duration_element.replaceWith(formatDuration(duration))
        var begin_time = 30;
        if (duration < 60 && duration >= 30) {
            begin_time = duration-30;
        } else if (duration < 30) {
            begin_time = 0;
        }
        audio.dataset.beginTime = begin_time;
        current_position_element.replaceWith(formatDuration(begin_time));
        player_progress.value = begin_time;

        audio.src = audioSrc;
        audio.play();
        audio.dataset.currentlyPlayingId = id;

        audio.ontimeupdate = (event) => {updatePlayerProgress(event);}
        audio.onended = (event) => {hidePlayer();};
    }    
}

function updatePlayerProgress(event) {
    var audio = document.querySelector("audio.player_audio");
    begin_time = audio.dataset.beginTime;
    var current_position_element = document.querySelector(
        ".player #player_current_time"
    ).firstChild;
    var player_progress = document.querySelector(
        ".player progress"
    )
    current_time = parseInt(begin_time) + parseFloat(audio.currentTime);
    current_position_element.replaceWith(
        formatDuration(current_time)
    );
    player_progress.value = current_time;
}

initPlayer();