import os
import web

production_mode = os.environ.get('PRODUCTION_MODE', False)
render = web.template.render('templates/', base='base', cache=production_mode)
render_plain = web.template.render('templates/', cache=production_mode) #without base, useful for sending mails

urls = (
  '', 'reblog',
  '/', 'index',
  '/feed', 'feed',
  '/(.*)', 'post',
)

content = [
  web.storage(
    slug='fecpvs',
    title='More data!',
    author='Aaron Swartz',
    updated='2008-07-30T00:00:00Z',
    body = """
<p>In his 1959 classic, <em>The Sociological Imagination</em>, the great sociologist C. Wright Mills told students of the discipline:</p>

<blockquote>
  <p>As a social scientist, you have to &#8230; capture what you experience and sort it out; only in this way can you hope to use it to guide and test your reflection, and in the process shape yourself as an intellectual craftsman. But how can you do this? One answer is: you must set up a blog&#8230;</p>
  
  <p>In such a blog &#8230; there is joined personal experience and professional activities, studies under way and studies planned. In this blog, you &#8230; will try to get together what you are doing intellectually and what you are experiencing as a person. here you will not be afraid to use your experience and relate it directly to various work in progress. By serving as a check on repetitious work, your blog also enables you to conserve your energy. It also encourages you to capture &#8216;fringe-thoughts&#8217;: various ideas which may be byproducts of everyday life, snatches of conversation overheard in the street, or, for that matter, dreams. Once noted, these may lead to more systematic thinking, as well as lend intellectual relevance to more directed experience.</p>
  
  <p>&#8230;The blog also helps you build up the habit of writing. &#8230; In developing the blog, you can experiment as a writer and this, as they say, develop your powers of expression.</p>
</blockquote>

<p>Actually, he called it a &#8220;file&#8221; instead of a blog, but the point remains the same: becoming a scientific thinker requires practice and writing is a powerful aid to reflection.</p>

<p>So that&#8217;s what this blog is. I write here about thoughts I have, things I&#8217;m working on, stuff I&#8217;ve read, experiences I&#8217;ve had, and so on. Whenever a thought crystalizes in my head, I type it up and post it here. I don&#8217;t read over it, I don&#8217;t show it to anyone, and I don&#8217;t edit it &#8212; I just post it.</p>

<p>I don&#8217;t consider this writing, I consider this thinking. I like sharing my thoughts and I like hearing yours and I like practicing expressing ideas, but fundamentally this blog is not for you, it&#8217;s for me. I hope that you enjoy it anyway.</p>


<p><i>You should follow me on twitter <a href="http://twitter.com/aaronsw">here</a>.</i></p>
"""
  )
]
content_mapping = dict((x.slug, x) for x in content)

class index:
    def GET(self):
        return render.blog_index(content)

class feed:
    def GET(self):
        web.header('content-type', 'application/atom+xml')
        lastupdate = max(x.updated for x in content)
        return render._template('blog_feed')(content, lastupdate)

class post:
    def GET(self, name):
        if name in content_mapping:
            return render.blog_post(content_mapping[name])
        else:
            raise web.notfound()

class reblog:
    def GET(self):
        raise web.seeother('/')

app = web.application(urls, globals())

wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
