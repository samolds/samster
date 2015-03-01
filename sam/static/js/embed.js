var embedIds = [];
var displayed = [];

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

function adjustEmpty() {
  var inbetween = document.getElementById('river-inbetween');
  var content = document.getElementById('river-content');
  if (displayed.length == 0) {
    content.style.display = "none";
    inbetween.style.display = "none";
  } else {
    inbetween.style.display = "block";
    content.style.display = "block";
  }
}

function toggleDisplay(className, fromButtonClick) {
    var elements = document.getElementsByClassName(className);
    var checked = document.getElementById(className + '-toggle').checked;
    for (var i = 0; i < elements.length; i++) {
        if (!checked) {
            elements[i].style.display = "none";
            displayed.pop(elements[i]);
        } else { 
            elements[i].style.display = "block";
            displayed.push(elements[i]);
        }
    }
    if (fromButtonClick) {
        adjustEmpty();
    }
    return checked;
}

function embed(embeds) {
    var ni = document.getElementById('embeds');
    embeds.forEach(function(embed) {
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
            lastfm(newdiv, embed);
        } else if (embed.type == "soundcloud") {
            soundcloud(newdiv, embed);
        } else if (embed.type == "flickr") {
            flickr(newdiv, embed);
        } else if (embed.type == "github") {
            github(newdiv, embed);
        } else if (embed.type == "twitter") {
            twitter(newdiv, embed);
        } else if (embed.type == "blog") {
            blog(newdiv, embed);
        } else if (embed.type == "imgur") {
            imgur(newdiv, embed);
        } else {
            simple(newdiv, embed);
        }
        if (priorLi) {
            ni.insertBefore(newdiv, priorLi);
        } else {
            ni.appendChild(newdiv);
        }
    });
    if (embeds.length > 0) {
        if (toggleDisplay(embeds[0].type, false)) {
            document.getElementById("hide").style.display = "none";
            document.getElementById("embeds").style.display = "block";
        }
    }
}

function lastfm(newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple lastfm');
    var embednowplaying = "Recently listened to";
    if (embed.nowplaying) {
        embednowplaying = "<i class=\"lastfmnp\">Now Playing!</i>";
    }
    newdiv.innerHTML = "<div class=\"right\">" + embednowplaying + " on <a href=\"http://last.fm/user/" + embed.USERNAME + "\">Last.fm</a></div><a href=\"" + 
                embed.url + "\">" + embed.name + " - " + embed.artist + "</a><div class=\"clear\"></div>";
}

function soundcloud(newdiv, embed) {
    newdiv.setAttribute('class', 'embedsc soundcloud');
    newdiv.innerHTML = embed.html;
}

function flickr(newdiv, embed) {
    newdiv.setAttribute('class', 'embed-photo flickr');
    var embedtitle = "";
    if (embed.title) {
        embedtitle = "<a href=\"http://flickr.com/photos/" + embed.USERNAME + "/" + embed.photoid + "\"><h3>" + embed.title + "</h3></a>";
    }
    var embeddescription = "";
    if (embed.description) {
        embeddescription = "<div class=\"flickrdesc\">" + embed.description + "</div>";
    }
    newdiv.innerHTML = "<a href=\"http://flickr.com/photos/" + embed.USERNAME + "/" + embed.photoid + "\"><img class=\"right\" src=\"" + embed.imgsrc + "\" /></a>" +
                "<div class=\"flickrdesc\">" + embedtitle + embeddescription + "<div>From <a href=\"http://flickr.com/" + embed.USERNAME + "\">Flickr</a></div>" +
                "</div><div class=\"clear\"></div>";
}

function github(newdiv, embed) {
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
    newdiv.innerHTML = "<div class=\"right\">From <a href=\"http://github.com/" + embed.USERNAME + "\">GitHub</a>" +
              "</div>" + embedeventtype + "<div class=\"clear\"></div>";
}

function twitter(newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple twitter');
    newdiv.innerHTML = embed.html;
    if (twttr && twttr.widgets) {
      twttr.widgets.load(newdiv);
    }
}

function blog(newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple blog');
    newdiv.innerHTML = "<h3><a href=\"" + embed.link + "\">" + embed.title + "</a></h3><div class=\"content\">" + 
              embed.stub + "<div class=\"clear\"></div></div><small>A recent <a href=\"/blog\">Blog Post</a></small>";
}

function imgur(newdiv, embed) {
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

function simple(newdiv, embed) {
    newdiv.setAttribute('class', 'embedsimple embedsimple');
    newdiv.innerHTML = embed.html;
}
