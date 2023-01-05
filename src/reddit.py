# Author: Shane Kelly


import praw
import random
import src.madlibs as madlibs
import time

def get_topic_comments (submission):
    """ (Submission) -> List<Comments>
    Takes as input a post on reddit and returns a list containing comment objects for each comment on that post.
    
    >>> url = 'https://www.reddit.com/r/mcgill/comments/eay2ne/mcgill_subreddit_bingo_finals_edition/'
    >>> submission = reddit.submission(url=url)
    >>> get_topic_comments(submission)
    [Comment(id='fb0vh26'), Comment(id='fb0l4dk'), Comment(id='fb15bvy'),
    Comment(id='fb1pwq8'), Comment(id='fb26drr'), Comment(id='fj2wd6x'),
    Comment(id='fb1spzv'), Comment(id='fb1td2g'), Comment(id='fb1trul')]
    """
    
    submission.comments.replace_more(limit=None)
    return submission.comments.list()

def filter_comments_from_authors (commentList, authorNames):
    """ (list<Comment>, list<string>) -> List<Comments>
    Takes a list of comments commentList and a list of strings authorNames, returns a list of comments that contains only comments made by users with names
    included in authorNames.
    
    >>> url = 'https://www.reddit.com/r/mcgill/comments/eay2ne/mcgill_subreddit_bingo_finals_edition/'
    >>> submission = reddit.submission(url=url)
    >>> comments = get_topic_comments(submission)
    >>> filter_comments_from_authors (comments, ["corn_on_the_cobh"])
    [Comment(id="fb0vh26")]
    """
    listHolder = []
    
    # Compares the two lists for instances where the author of the comment is found within the list of names.
    
    for x in commentList:
        if str(x.author) in authorNames:
            listHolder.append(x)
            
    return listHolder

def filter_out_comments_replied_to_by_authors (commentList, authorNames):
    """ (list<Comment>, list<string>) -> List<Comments>
    Takes input commentList containing a list of comments, and a list of strings authorNames and returns a list containing comments only that have not been made
    or replied to by a user with a name within authorNames.
    
    >>> url = 'https://www.reddit.com/r/mcgill/comments/eay2ne/mcgill_subreddit_bingo_finals_edition/'
    >>> submission = reddit.submission(url=url)
    >>> comments = get_topic_comments(submission)
    >>> filter_comments_from_authors (comments, ["corn_on_the_cobh"])
    [Comment(id='fb0l4dk'), Comment(id='fb15bvy'), Comment(id='fb1pwq8'), Comment(id='fb26drr'), Comment(id='fj2wd6x'),
    Comment(id='fb1spzv'), Comment(id='fb1td2g'), Comment(id='fb1trul')]
    """
    listHolder = []
    
    # Loop within a loop to check for the replies of every individual checked comment.
    
    for x in commentList:
        if x.author not in authorNames:
            listHolder.append(x)
            
            for y in x.replies:
                if y.author in authorNames:
                    listHolder.remove(x)
                    break
                
    return listHolder
    
def get_authors_from_topic (submission):
    """ (Submission) -> List<string>
    Takes a submission as input and returns a list of the names of every user that has commented on or replied to comments on this submission.
    
    >>> url = 'https://www.reddit.com/r/frogs/comments/tpc53q/happy_saturday_from_waffles/'
    >>> submission = reddit.submission(url=url)
    >>> get_authors_from_topic (submission)
    ["TheAngriestAtheist","Creepy_Ant_8825","YuBandCharleyfan_alt","Juedequilles"]
    """
    nameLibrary = dict()
    commentList = get_topic_comments(submission)
    
    for x in commentList:
        nameLibrary[str(x.author)] = len(filter_comments_from_authors(commentList, str(x.author)))
         
    return nameLibrary
    
def select_random_submission_url (reddit, topicURL, subreddit, replacelim):
    """ (Reddit, string, string, int) -> string
    Takes a reddit object, a topicURL, a subreddit, and a replace limiter. Rolls a die, on a 1 or 2 returns the submission contained within topicURL,
    else returns a random submission from subreddit, checking the top posts up to replacelim.
    """
    diceroll = random.randint(1, 6)
    randomChooser = []
    
    if diceroll == 1 or diceroll == 2:
        return reddit.submission(url=topicURL)
    else:
        for submission in reddit.subreddit(subreddit).hot(limit=replacelim):
            randomChooser.append(submission)
        return randomChooser[random.randint(0, len(randomChooser) - 1)]

def post_reply (submission, username):
    """ (Submission, string) -> None
    Takes a submission on reddit, as well as a string containing the username of the bot. Returns nothing, but makes an automatically generated post to the inputted
    submission.
    """
    
    # If no comment has been posted by the bot, post a comment.
    
    if username not in get_authors_from_topic(submission):
        submission.reply(madlibs.generate_comment())
    
    # If a post has been posted by the bot, reply to an existing comment.
    
    else:
        potential_replies = filter_out_comments_replied_to_by_authors (get_topic_comments(submission), [username])
        potential_replies[random.randint(0, len(potential_replies) - 1)].reply(madlibs.generate_comment())
        
def bot_daemon (reddit, startURL, replaceLim, subredditName, username):
    """ (reddit, string, int, string, string) -> None
    Takes a reddit upject, a starting URL, a replace limiter, a subreddit name, and the name of the bot, and loops endlessly causing the bot to post randomly generated
    messages to the inputted subreddit, starting at the post tied to the startURL.
    """
    
    # INFINITE LOOP! Will run forever until stop is clicked.
    
    while True:
        submission = select_random_submission_url(reddit, startURL, subredditName, replaceLim)
        post_reply(submission, username)
        time.sleep(60)

if __name__ == '__main__' :
    reddit = praw.Reddit('bot', config_interpolation="basic")    