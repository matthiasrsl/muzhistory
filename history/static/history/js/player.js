var playerProgressBar;

function initPlayer() {
    var player_album_cover = document.querySelector(
        ".player .album_cover"
    );
    player_album_cover.onclick = "";
    player_album_cover.firstElementChild.title = "";
}

function LightenDarkenColor(col, amt) {
    var usePound = false;
    if (col[0] == "#") {
        col = col.slice(1);
        usePound = true;
    }
    var num = parseInt(col, 16);
    var r = (num >> 16) + amt;
    if (r > 255) r = 255;
    else if (r < 0) r = 0;
    var b = ((num >> 8) & 0x00FF) + amt;
    if (b > 255) b = 255;
    else if (b < 0) b = 0;
    var g = (num & 0x0000FF) + amt;
    if (g > 255) g = 255;
    else if (g < 0) g = 0;
    return (usePound ? "#" : "") + (g | (b << 8) | (r << 16)).toString(16);
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
    var player = document.querySelector(".player");
    var audio = document.querySelector("audio.player_audio");

    if (audio.dataset.currentlyPlayingId == id) {
        if (audio.paused) {
            audio.play();
        } else {
            audio.pause()
        }
    } else {
        if (playerProgressBar) {
            playerProgressBar.destroy();
        }

        // Album cover.
        var album_cover_url = document.querySelector("#track_" + id + " img").src;
        var player_album_cover = document.querySelector(
            ".player .album_cover img"
        );
        player_album_cover.src = album_cover_url;

        // Track metadata
        var track_metadata = document.querySelector(
            "#track_" + id + " .track_metadata"
        ).cloneNode(true);
        var player_track_metadata = document.querySelector(
            ".player .track_metadata"
        );
        player_track_metadata.replaceWith(track_metadata);
        var album_name = document.querySelector(".player .album_name");
        if (album_name != null) {
            document.querySelector(".player .additional_info").remove();
        }

        // Duration
        var duration = document.querySelector("#track_" + id).dataset.duration;
        player.dataset.duration = duration;
        var begin_time = 30;
        if (duration < 60 && duration >= 30) {
            begin_time = duration - 30;
        } else if (duration < 30) {
            begin_time = 0;
        }
        
        // Total Duration text
        var total_duration_element = document.querySelector(
            ".player #player_total_time"
        ).firstChild;
        total_duration_element.replaceWith(formatDuration(duration))

        // Current position
        var current_position_element = document.querySelector(
            ".player #player_current_time"
        ).firstChild;
        current_position_element.replaceWith(formatDuration(begin_time));

        // Progress abr and colors
        var progress_container = document.querySelector(".progress_container");
        vibrant = Vibrant.from(album_cover_url);
        vibrant.getPalette((err, palette) => {
            var bg_color = tinycolor(palette.LightVibrant.hex)
            var bg_color_alt = tinycolor(palette.LightMuted.hex)
            if (bg_color.getBrightness() > 240) {
                player.style.background = bg_color_alt;
            } else {
                player.style.background = bg_color.desaturate(30).lighten(10);
            }
            nodes = Array.prototype.slice.call(
                track_metadata.childNodes
            ).concat(
                Array.prototype.slice.call(
                    document.querySelectorAll(".player p")
                )
            );
            nodes_featured_artists = document.querySelectorAll(
                ".player .artist_name_role_feat"
            );
            console.log(nodes_featured_artists);
            var text_color = tinycolor(palette.DarkMuted.hex).darken(10);
            var text_color_light = text_color.clone().lighten(20);
            for (var i = 0; i < nodes.length; i++) {
                if (nodes[i].nodeType === Node.ELEMENT_NODE) {
                    nodes[i].style.color = text_color;
                }
            }
            for (var i = 0; i < nodes_featured_artists.length; i++) {
                if (nodes_featured_artists[i].nodeType === Node.ELEMENT_NODE) {
                    nodes_featured_artists[i].style.color = text_color_light;
                }
            }
            var bar = new ProgressBar.Line(progress_container, {
                strokeWidth: 4,
                easing: 'easeInOut',
                duration: 1,
                color: tinycolor(palette.Muted.hex).saturate(100),
                trailColor: tinycolor(palette.LightVibrant.hex).darken(10).desaturate(60),
                trailWidth: 1,
                svgStyle: { width: '100%', height: '100%' }
            });
            playerProgressBar = bar;
        });

        // Audio
        var audioSrc = document.querySelector("#track_" + id).dataset.audioSrc;
        audio.src = audioSrc;
        audio.play();
        audio.dataset.currentlyPlayingId = id;
        audio.dataset.beginTime = begin_time;
        audio.ontimeupdate = (event) => { updatePlayerProgress(event); }
        audio.onended = (event) => { hidePlayer(); };
    }
}

function updatePlayerProgress(event) {
    var player = document.querySelector(
        ".player"
    )
    var audio = document.querySelector("audio.player_audio");
    var begin_time = audio.dataset.beginTime;
    var duration = player.dataset.duration;
    var current_position_element = document.querySelector(
        ".player #player_current_time"
    ).firstChild;
    current_time = parseInt(begin_time) + parseFloat(audio.currentTime);
    current_position_element.replaceWith(
        formatDuration(current_time)
    );
    playerProgressBar.set(current_time / duration);
}

initPlayer();