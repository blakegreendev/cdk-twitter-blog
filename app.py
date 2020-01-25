#!/usr/bin/env python3

from aws_cdk import core

from twitter_blog.twitter_blog_stack import TwitterBlogStack


app = core.App()
TwitterBlogStack(app, "twitter-blog")

app.synth()
