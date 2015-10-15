# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort
from DelogX import app, api, config

@app.route('/')
def index():
    return number(1)

@app.route(config.site_info['POST_LIST_URL'] + '<int:pid>/')
def number(pid):
    import time
    import urllib
    post_list, max_number = api.get_post_list(pid)
    if post_list is None:
        abort(404)
    else:
        for post in post_list:
            if post:
                post['url'] = urllib.quote(post['url'])
                post['time'] = time.strftime(config.site_info['TIME_FORMAT'],
                    time.localtime(float(post['time'])))
        prev_page = True
        next_page = True
        if pid == 1:
            prev_page = False
        if pid == max_number:
            next_page = False
        return render_template('list.html',
            site_config=config.site_info, header=api.get_header(), post_list=post_list,
                pid=pid, prev_page=prev_page, next_page=next_page)

@app.route(config.site_info['POST_URL'] + '<postid>/')
def posts(postid):
    import time
    import urllib
    postid = urllib.unquote(postid).encode('utf-8')
    post_info = api.get_post(postid)
    if post_info:
        post_info['url'] = urllib.quote(post_info['url'])
        post_info['time'] = time.strftime(config.site_info['TIME_FORMAT'],
            time.localtime(float(post_info['time'])))
        return render_template('posts.html',
            site_config=config.site_info, header=api.get_header(), post=post_info)
    else:
        abort(404)

@app.route(config.site_info['PAGE_URL'] + '<pageid>/')
def pages(pageid):
    import urllib
    pageid = urllib.unquote(pageid).encode('utf-8')
    page_info = api.get_page(pageid)
    if page_info:
        page_info['url'] = urllib.quote(page_info['url'])
        return render_template('pages.html',
            site_config=config.site_info, header=api.get_header(), page=page_info)
    else:
        abort(404)

#del
@app.route('/u/')
def u():
    api.update_list()
    return repr(api.global_pages) + "<br>" + repr(api.global_posts)+'<br>'

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',
        site_config=config.site_info, header=api.get_header())