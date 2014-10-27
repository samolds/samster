var embedIds = [];

// Requires jQuery
function ajaxCall(embedType) {
  $.ajax({
    type: "GET",
    url: "/river/async/" + embedType,
    success: function(data) {
      embed(data);
    },
    error: function() {
      console.log(embedType + ' failed to load');
    }
  })
}

function toggleDisplay(className) {
    var elements = document.getElementsByClassName(className);
    var checked = document.getElementById(className + '-toggle').checked;
    for (var i = 0; i < elements.length; i++) {
        if (!checked) {
            elements[i].style.display = "none";
        } else { 
            elements[i].style.display = "block";
        }
    }
    return checked;
}

function embed(data) {
    var ni = document.getElementById('embeds');
    data.embeds.forEach(function(embed) {
        var newdiv = document.createElement('li');
        newdiv.setAttribute('id', embed.date);
        newdiv.setAttribute('title', embed.print_date);
        embedIds.push(embed.date);
        embedIds.sort(function(a, b) {
          return b - a;
        });
        var index = embedIds.indexOf(embed.date);
        var priorLi = null;
        if (index > 0) {
            priorLi = document.getElementById(embedIds[index - 1]);
        } else if (index == 0) {
            priorLi = document.getElementById(embedIds[index]);
        }
        if (embed.type == "lastfm") {
            lastfm(data, newdiv, embed);
        } else if (embed.type == "soundcloud") {
            soundcloud(data, newdiv, embed);
        } else if (embed.type == "flickr") {
            flickr(data, newdiv, embed);
        } else if (embed.type == "github") {
            github(data, newdiv, embed);
        } else if (embed.type == "twitter") {
            twitter(data, newdiv, embed);
        } else if (embed.type == "blog") {
            blog(data, newdiv, embed);
        } else if (embed.type == "imgur") {
            imgur(data, newdiv, embed);
        } else {
            simple(data, newdiv, embed);
        }
        if (priorLi) {
            ni.insertBefore(newdiv, priorLi);
        } else {
            ni.appendChild(newdiv);
        }
    });
    if (data.embeds.length > 0) {
        if (toggleDisplay(data.embeds[0].type)) {
            document.getElementById("hide").style.display = "none";
            document.getElementById("embeds").style.display = "block";
        }
    }
}

function lastfm(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple lastfm');
    var embednowplaying = "Recently listened to";
    if (embed.nowplaying) {
        embednowplaying = "<i class=\"lastfmnp\">Now Playing!</i>";
    }
    newdiv.innerHTML = "<div class=\"right\">" + embednowplaying + " on <a href=\"http://last.fm/user/" + data.USERNAME + "\">Last.fm</a></div><a href=\"" + 
                embed.url + "\">" + embed.name + " - " + embed.artist + "</a><div class=\"clear\"></div>";
}

function soundcloud(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embedsc soundcloud');
    newdiv.innerHTML = embed.html;
}

function flickr(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embed-photo flickr');
    var embedtitle = "";
    if (embed.title) {
        embedtitle = "<a href=\"http://flickr.com/photos/" + data.USERNAME + "/" + embed.photoid + "\"><h3>" + embed.title + "</h3></a>";
    }
    var embeddescription = "";
    if (embed.description) {
        embeddescription = "<div class=\"flickrdesc\">" + embed.description + "</div>";
    }
    newdiv.innerHTML = "<a href=\"http://flickr.com/photos/" + data.USERNAME + "/" + embed.photoid + "\"><img class=\"right\" src=\"" + embed.imgsrc + "\" /></a>" +
                "<div class=\"flickrdesc\">" + embedtitle + embeddescription + "<div>From <a href=\"http://flickr.com/" + data.USERNAME + "\">Flickr</a></div>" +
                "</div><div class=\"clear\"></div>";
}

function github(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple github');
    var embedeventtype = "<p>Did some GitHub activity</p>";
    if (embed.event_type == "PushEvent") {
        embedeventtype = "";
        embed.payload.commits.forEach(function(commit) {
            embedeventtype += "<a href=\"" + embed.repo_url + "/commit/" + commit.sha + "\"><i>" + commit.sha + "</i></a>:" +
            "<p class=\"space\">" + commit.message + "</p>";
        });
        embedeventtype += "<p>Pushed to <a href=\"" +  embed.repo_url + "\">" + embed.repo.name + "</a></p>";
    } else if (embed.event_type == "WatchEvent") {
        embedeventtype = "<p>Started watching <a href=\"" + embed.repo_url + "\">" + embed.repo.name + "</a></p>";
    } else if (embed.event_type == "CreateEvent") {
        var description = "";
        if (embed.payload.description) {
            description = "<p class=\"space\">" + embed.payload.description + "</p>";
        }
        var ref = embed.payload.ref;
        if (!ref) {
            ref = "<a href=\"" + embed.repo_url + "\">" + embed.repo.name + "</a>";
        }
        embedeventtype = "<p>Created new " + embed.payload.ref_type + ": <i>" + ref + "</i>" + description + 
            "</p>On <a href=\"" + embed.repo_url +"\">" + embed.repo.name + "</a>";
    } else if (embed.event_type == "CommitCommentEvent") {
        embedeventtype = "<p>Commented on commit <a href=\"" + embed.payload.comment.html_url + "\">" + embed.payload.comment.commit_id + "</a>:" +
                  "<p class=\"space\">" + embed.payload.comment.body + "</p></p>";
    } else if (embed.event_type == "GollumEvent") {
        embedeventtype = "<p>Edited<p class=\"space\">";
        embed.payload.pages.forEach(function(page) {
            embedeventtype += "<p><a href=\"" + page.html_url + "\">" + page.title + "</a></p>";
        });
        embedeventtype += "</p>On <a href=\"" + embed.repo_url + "\">" + embed.repo.name + "</a></p>";
    }
    newdiv.innerHTML = "<div class=\"right\">From <a href=\"http://github.com/" + data.USERNAME + "\">GitHub</a>" +
              "</div>" + embedeventtype + "<div class=\"clear\"></div>";
}

function twitter(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple twitter');
    newdiv.innerHTML = embed.html;
}

function blog(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple blog');
    newdiv.innerHTML = "<h3><a href=\"" + embed.link + "\">" + embed.title + "</a></h3><div class=\"content\">" + 
              embed.stub + "<div class=\"clear\"></div></div><small>A recent <a href=\"/blog\">Blog Post</a></small>";
}

function imgur(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embed-photo imgur');
    var embedtitle = "";
    if (embed.title) {
        embedtitle = "<h3>" + embed.title + "</h3>";
    }
    var favorited = "Favorited image on ";
    if (embed.is_album) {
        favorited = "Favorited album on ";
    }
    newdiv.innerHTML = "<a href=\"" + embed.link + "\">" + embedtitle + "<img src=\"" + embed.imgsrc + "\" /></a>" +
                "<div>" + favorited + "<a href=\"http://imgur.com\">Imgur</a></div>" +
                "<div class=\"clear\"></div>";
}

function simple(data, newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple embedsimple');
    newdiv.innerHTML = embed.html;
}
