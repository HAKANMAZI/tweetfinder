# pip install flask
# pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git
# pip install pandas

from flask import Flask, render_template, request, url_for, redirect, send_file, session
from requests import post
import snscrape.modules.twitter as twitter
import pandas as pd
import os 

def delete_csv():
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".csv"):
            print(item)
            os.remove(os.path.join(dir_name, item))


from datetime import datetime
from datetime import timedelta
class ScrapeTweets():
    def __init__(self) -> None:
        self.yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        self.tomorrow = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
        self.posts = []

    def post_times(self):
        times = {
            "yesterday" : self.yesterday,
            "tomorrow" : self.tomorrow
        }
        post_times.append(times)
        return post_times


    def trending_tweets_url(self, keyword, like_count=50, sincetime="", untiltime=""):
        ''' Bu kelime hangi tweette geçiyor onları scrape etmek için'''
        counter = 0
        self.posts = []
        for i, tweet in enumerate(twitter.TwitterSearchScraper(keyword + ' since:'+sincetime+' until:'+untiltime).get_items()):
            if tweet.likeCount > like_count:
                if counter == 3: break
                print(self.yesterday)
                print(self.tomorrow)
                print(tweet.url)

                tweet = {
                'username': tweet.user.username,
                'content': tweet.content,
                'date_posted': tweet.date,
                'url': tweet.url
                }
                self.posts.append(tweet)
                counter +=1
        return self.posts
        

    def userTweets(self, username='',keyword='' , like_count=0, sincetime="", untiltime=""):
        counter = 0
        self.posts = []
        for i, tweet in enumerate(twitter.TwitterSearchScraper('from:'+username+' '+keyword+' since:'+sincetime+' until:'+untiltime).get_items()):
            if tweet.likeCount >= like_count:
                if counter == 3: break
                print(self.yesterday)
                print(self.tomorrow)
                print(tweet.url)

                tweet = {
                'username': tweet.user.username,
                'content': tweet.content,
                'date_posted': tweet.date,
                'url': tweet.url
                }
                self.posts.append(tweet)
                counter +=1


cls=ScrapeTweets()
post_times = []
post_times = cls.post_times()


app = Flask(__name__)
app.config['SECRET_KEY'] = "DemoString"

@app.route("/", methods=['GET','POST'])
def index():
    return render_template("index.html")

# @app.route("/login", methods=['GET','POST'])
# def login():
#     return render_template("index.html")
# 
# @app.route("/register", methods=['GET','POST'])
# def register():
#     return render_template("index.html")



@app.route("/index", methods=['GET','POST'])
def trending_tweets_url():
    delete_csv()
    posts = []
    if request.method == 'POST':
        session['Username'] = request.form.get('Username')
        session['TweetWord'] = request.form.get('TweetWord')
        session['like_count'] = request.form.get('like_count')
        session['sincetime'] = request.form.get('sincetime')
        session['untiltime'] = request.form.get('untiltime')

        if session['keyword']:
            posts = cls.userTweets(session['Username'],session['TweetWord'], int(session['like_count']), session['sincetime'], session['untiltime'] )

    print(post_times) 
    print(posts)   
    return render_template('index.html', post_times=post_times, posts = posts)
    

if __name__=="__main__":
    app.run(debug=True)
