from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from sam.models import Post
from django.db.models import Q
from django.core.cache import cache
from TwitterAPI import TwitterAPI
from django.conf import settings
from datetime import datetime, timedelta
import simplejson as json
import soundcloud
import flickrapi
#import facebook
import markdown
import github3
import oauth2


def river(request):
    return render_to_response('river.html', context_instance=RequestContext(request))


def embeds(embeds):
    too_old = []
    no_older_than = 90
    for embed in embeds:
        embed['date'] = embed['date'].replace(tzinfo=None)
        if embed['date'] < (datetime.now() - timedelta(days=no_older_than)):
            too_old.append(embed)
    for item in too_old:
        embeds.remove(item)

    future = datetime.now() + timedelta(days=7)
    for embed in embeds:
        embed['print_date'] = datetime.strftime(embed['date'], "%b %d, %Y %I:%M %p")
        embed['date'] = int((future - embed['date']).total_seconds())
        if (embed['type'] == "lastfm" and embed['nowplaying']):
            embed['date'] = 0

    return HttpResponse(json.dumps(embeds), content_type="application/json")


# BLOGS
def blogs(request):
    blogs = cache.get("blogs")
    if not blogs:
        blogs = []
        try:
            public = Q(private=False)
            blog_posts = Post.objects.order_by('-creation_date').filter(public)
            if len(blog_posts) > 5:
                blog_posts = blog_posts[:5]
            for blog in blog_posts:
                blogs.append({
                    "type": "blog",
                    "date": blog.creation_date,
                    "link": "/blog/post/%d" % blog.pk,
                    "title": blog.title,
                    "stub": blog.small_stub,
                })
            cache.set("blogs", blogs, 60 * 60)
        except:
            pass
    return embeds(blogs)


# TWITTER
def twitters(request):
    embedded_tweets = cache.get("twitters")
    if not embedded_tweets:
        embedded_tweets = []
        try:
            t = settings.TWITTER
            api = TwitterAPI(t['CONSUMER_KEY'], t['CONSUMER_SECRET'], t['ACCESS_TOKEN_KEY'], t['ACCESS_TOKEN_SECRET'])
            tweets = api.request('statuses/user_timeline', {'count': 10})
            tweet_dict = json.loads(tweets.text)
            for tweet in tweet_dict:
                tweet_json = api.request('statuses/oembed', {'id': "%d" % tweet['id'], "omit_script": "true"})
                tweet_html = json.loads(tweet_json.text)
                tweet_created_at = tweet['created_at'].split(" +0000")
                tweet_created_at = "%s%s" % (tweet_created_at[0], tweet_created_at[1])
                tweet_created_at = datetime.strptime(tweet_created_at, "%a %b %d %H:%M:%S %Y")
                tweet_html.update({"date": tweet_created_at, "type": "twitter"})
                embedded_tweets.append(tweet_html)
            cache.set("twitters", embedded_tweets, 60 * 60 * 2)
        except:
            pass
    return embeds(embedded_tweets)


# SOUNDCLOUD
def soundclouds(request):
    embedded_tracks = cache.get("soundclouds")
    if not embedded_tracks:
        embedded_tracks = []
        try:
            sc = settings.SOUNDCLOUD
            client = soundcloud.Client(client_id=sc['CLIENT_ID'])
            tracks = client.get('/users/' + sc['USER_ID'] + '/favorites', limit=10)
            for track in tracks:
                e_track = client.get('/oembed', url=track.obj['uri'])
                track_created_at = track.obj['created_at'].split(" +0000")
                track_created_at = "%s%s" % (track_created_at[0], track_created_at[1])
                track_created_at = datetime.strptime(track_created_at, "%Y/%m/%d %H:%M:%S")
                e_track.obj.update({"date": track_created_at, "type": "soundcloud"})
                embedded_tracks.append(e_track.obj)
            cache.set("soundclouds", embedded_tracks, 60 * 60 * 24 * 5)
        except:
            pass
    return embeds(embedded_tracks)


# LAST.FM
def lastfms(request):
    lastfmtracks = cache.get("lastfms")
    if not lastfmtracks:
        lastfmtracks = []
        try:
            lfm = settings.LASTFM
            lastfmkey = lfm['KEY']
            lastfmsecret = lfm['SECRET']
            consumer = oauth2.Consumer(key=lastfmkey, secret=lastfmsecret)
            client = oauth2.Client(consumer)

            url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + lfm['USERNAME'] + "&format=json&limit=%d&api_key=%s" % (29, lastfmkey)

            resp, content = client.request(url, 'GET')
            lastfmtracks = json.loads(content)['recenttracks']['track']
            if type(lastfmtracks) == dict:
                lastfmtracks = [lastfmtracks]
            for track in lastfmtracks:
                if '@attr' in track and track['@attr'] == {'nowplaying': 'true'}:
                    date = datetime.now()
                    track.update({"nowplaying": True})
                else:
                    date = datetime.strptime(track['date']['#text'], '%d %b %Y, %H:%M')
                    track.update({"nowplaying": False})
                track.update({"artist": track['artist']['#text'], "date": date, "type": "lastfm", "USERNAME": lfm['USERNAME']})
            cache.set("lastfms", lastfmtracks, 60 * 1)
        except:
            pass
    return embeds(lastfmtracks)


# FLICKR
def flickrs(request):
    flickrs = cache.get("flickrs")
    if not flickrs:
        flickrs = []
        try:
            f = settings.FLICKR
            usr = f['USERNAME']
            flickr = flickrapi.FlickrAPI(f['KEY'])
            all_photos = flickr.photos_search(user_id=f['USER_ID'], per_page='10')
            for photos in all_photos:
                for photo in photos:
                    farm = photo.attrib['farm']
                    s_id = photo.attrib['server']
                    p_id = photo.attrib['id']
                    p_secret = photo.attrib['secret']
                    info = flickr.photos_getInfo(photo_id=p_id, format="xmlnode")
                    p_date = datetime.fromtimestamp(int(info.photo[0].dates[0].attrib['posted']))
                    description = markdown.markdown(info.photo[0].description[0].text)
                    title = info.photo[0].title[0].text
                    photolink = "http://farm%s.staticflickr.com/%s/%s_%s_n.jpg" % (farm, s_id, p_id, p_secret)
                    flickrs.append({"imgsrc": photolink, "photoid": p_id, "date": p_date, "type": "flickr", "description": description, "title": title, "USERNAME": usr})
            cache.set("flickrs", flickrs, 60 * 60 * 12)
        except:
            pass
    return embeds(flickrs)


# GITHUB
def githubs(request):
    githubs = cache.get("githubs")
    if not githubs:
        githubs = []
        try:
            gh = settings.GITHUB
            me = github3.user(gh['USERNAME'])
            consumer = oauth2.Consumer(key="", secret="")
            client = oauth2.Client(consumer)
            resp, content = client.request(me.events_urlt.expand(), 'GET')
            events = json.loads(content)
            for event in events:
                git_event = event
                date = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                e_type = event['type']
                git_event.update({"repo_url": "http://github.com/%s" % (event['repo']['name'])})
                git_event.update({"date": date, "type": "github", "event_type": e_type, "USERNAME": gh['USERNAME']})
                githubs.append(git_event)
            cache.set("githubs", githubs, 60 * 60)
        except:
            pass
    return embeds(githubs)



# IMGUR
def imgurs(request):
    imgurs = cache.get("imgurs")
    if not imgurs:
        imgurs = []
        try:
            i_client = settings.IMGUR['CLIENT_ID']
            i_secret = settings.IMGUR['SECRET']
            i_code = settings.IMGUR['ACCESS_CODE']
            i_username = settings.IMGUR['USERNAME']

            consumer = oauth2.Consumer(key='', secret='')
            client = oauth2.Client(consumer)
            
            toGetCodeUrl = "https://api.imgur.com/oauth2/authorize?client_id=%s&response_type=token" % i_client

            params = "client_id=%s&client_secret=%s&grant_type=%s&code=%s" % (i_client, i_secret, "authorization_code", i_code)
            resp, content = client.request('https://api.imgur.com/oauth2/token', method='POST', body=params)
            token = json.loads(content)['access_token']

            #x, y = client.request(toGetCodeUrl, method='GET')
            #import pdb; pdb.set_trace()

            url = "https://api.imgur.com/3/account/%s/favorites" % i_username
            resp, content = client.request(url, 'GET', headers={"Authorization": "Bearer %s" %token})

            favorites = json.loads(content)['data']
            for favorite in favorites:
                uploaded_at = datetime.fromtimestamp(int(favorite['datetime']))
                imgur = {"title": favorite['title'], "date": uploaded_at, "type": "imgur", "is_album": favorite['is_album'], "USERNAME": i_username}
                if favorite['is_album']:
                    imgur.update({"imgsrc": "http://imgur.com/%s.gif" % favorite['cover'], "link": favorite['link']})
                else:
                    imgur.update({"imgsrc": favorite['link'], "link": "http://imgur.com/%s" % favorite['id']})
                imgurs.append(imgur)
            cache.set("imgurs", imgurs, 60 * 60)
        except:
            pass
    return embeds(imgurs)


# FACEBOOK - ABANDON...
def facebooks(request):
    facebooks = cache.get("facebooks")
    if not facebooks:
        facebooks = []
        try:
            key = ""
            secret = ""
            # short_token = just taken user token and figure out what to do, even though it expires...
            # token = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" % (key, secret, short_token)
            # graph = facebook.GraphAPI(token)
            # me = graph.get_object("me")

            #key = 
            #secret = 
            #for x in y:
            #githubs.append({"imgsrc": photolink, "photoid": p_id, "date": p_date, "type": "flickr", "description": description, "title": title})
            #cache.set("facebooks", facebooks, 60 * 60)
        except:
            pass
    return embeds(facebooks)
