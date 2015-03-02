User Guide
==========
There is very little hardcoded into this site in terms of content. Almost every single page is loaded from the database as a "blog post".

Some things to know:
--------------------
* When adding a "Post", markdown is used to convert the content of the post into html to be displayed
* There is a field to put embedded links (like youtube videos) in the blog post.
* Blog posts can have multiple images associated with it
* Tags are used quite abundantly. There are a handful of hardcoded tags that are used to distinguish a "blog post" from a "static page" even though they are from the same data model.
* The tags that are used for "static pages" are preceded by "top_". There are also a few tags ("projects", "work", "experience") that are hardcoded in the nav_bar to the post filter section.
* The most recently created blog post with a "top_" tag will be what is displayed as the "static page".
* Images with a "banner_photo" tag will be selected at random to be displayed on the home page, unless the current "top_home" post has an image that has the "banner_photo" tag. Then only that image will be used.
* The /blog page will only show the 5 most recent posts, but there is an archive page that groups posts by months and shows them all.
* There are three management commands for importing data. The first will generate all of the hardcoded tags. You can of course create any additional ones. There are also text file examples for 'quotes' and 'websites' for mass importing in sam/management/commands

    ```
    python manage.py tags
    python manage.py quotes
    python manage.py websites
    ```

* Almost all of the text values that show up, such as "sitename" or "username" are set in local_settings.py
* The River is the crown and jewel of this site. It can make API calls to Twitter, Flickr, Last.fm, GitHub, and Soundcloud to pull in some of the most recent activity from you and feed back into a single stream. All that is required to get this working is to add all of the information specified in local_settings.py for each of the sites. The most recent blog posts from this site will also be displayed in The River.
