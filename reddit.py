import json
import praw
import logging
import requests
import datetime
import time
import csv

# Opening json file for credentials
with open('credentials.json') as f:
    parameters = json.load(f)

# Bot bio
bot_name = 'Reddit information bot'
bot_version = '1.1 version'
bot_author = '/u/ivan1_'


# Configuring praw object
reddit = praw.Reddit(client_id=parameters['client_id'],
                    client_secret=parameters['api_key'],
                    password=parameters['password'],
                    user_agent=f'This is {bot_name}. It is in {bot_version}. Author of this bot is {bot_author}',
                    username=parameters['username'],
                    config_interpolation="basic")


# Printing all bot features
print("""
    For now this bot has 5 features:
        - bot_info();
        - subreddit_info()
        - dataMining_post()
        - redditor_info()
""")

print("To see more about the functions and how to run them type: help(function)")


# Observing http request
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)





# Information about bot
def bot_info():
    """ Function to introduce the bot.
        No arguments
    """
    print(reddit.config.user_agent)


# Information about subreddit
def subreddit_info(file='',subr=''):
    """ Function for getting information about one or more subreddits.
        Arguments(optional[file], optional[subr])
        You must enter 1 argument.
    """

    # Headers for the csv file
    headlines = ['Subreddit name','Subreddit title','Total subscribers',
                'Creation time','Subreddit id','Over 18', 'Public Description']

    # Checks if both arguments are empty
    if file == '' and subr == '':
        print("Please run the function with at least 1 argument.")
        return

    # Checks if only one subreddit is submitted for analyzing
    elif file == '':
        with open('subreddit.csv','w',newline='') as file:
            subreddit = reddit.subreddit(subr)
            name = 'r/' + subreddit.display_name
            old = time.ctime(subreddit.created_utc)
            writer = csv.DictWriter(file,fieldnames=headlines)
            writer.writeheader()
            writer.writerow({'Subreddit name':name,'Subreddit title':subreddit.title,'Total subscribers': subreddit.subscribers,'Creation time': old,
                            'Subreddit id': subreddit.id, 'Over 18': subreddit.over18,'Public Description': subreddit.public_description})

    else:
        try:

            # Splitting the text file into arrays
            f = open(file)
            whole_file = f.read()
            subs = whole_file.split()

            # Opening csv file to push data from subreddits
            with open('subreddits.csv','w',newline='') as file:

                writer = csv.DictWriter(file,fieldnames=headlines)
                writer.writeheader()

                # Iterating through every subreddit
                for sub in subs:
                    subreddit = reddit.subreddit(sub)
                    name = 'r/' + subreddit.display_name
                    old = time.ctime(subreddit.created_utc)
                    writer.writerow({'Subreddit name':name,'Subreddit title':subreddit.title,'Total subscribers': subreddit.subscribers,'Creation time': old,
                                    'Subreddit id': subreddit.id, 'Over 18': subreddit.over18,'Public Description': subreddit.public_description})

        # Catching the error
        except OSError:
            print("Please type in correct file with reddit usernames.")



# Basic analysis on hot posts
def dataMining_post(subr):
    """ Getting information for one or more posts.
        Arguments(subreddit)
    """
    # Initializing subreddit
    subreddit = reddit.subreddit(subr)

    # Opening csv file to store information about
    with open('data.csv','w',newline='') as file:
        headlines = ['Author','Creation time','Title','Total upvotes','Total comments','Spoiler','Link flair','URL']
        writer = csv.DictWriter(file,fieldnames=headlines)
        writer.writeheader()

        # Local funtion to analyze posts faster without repetitive code
        def writing_csv(post_type):
            #Looping through every post and writing data to csv file
            for post in post_type:
                old = time.ctime(post.created_utc)
                writer.writerow({'Author': post.author,'Creation time': old,'Title':post.title,
                'Total upvotes':post.score,'Total comments':post.num_comments,
                'Spoiler':post.spoiler,'Link flair':post.link_flair_text,'URL': post.url})

        # Declaring every type of posts
        posts = int(input("How many posts do you want to analyze? "))
        hot = subreddit.hot(limit=posts)
        rising = subreddit.rising(limit=posts)
        top = subreddit.top(limit=posts)
        new = subreddit.new(limit=posts)
        choice = input("What posts do you want to analze: hot, rising, top, or new: ")

        # Checking what posts the user wants to analyze and runs the local function to analyze the posts
        if choice == 'hot':
            writing_csv(hot)
        elif choice == 'rising':
            writing_csv(rising)
        elif choice == 'top':
            writing_csv(top)
        elif choice == 'new':
            writing_csv(new)
        else:
            print("Please choose one type of posts.")




#Analayzing through one or many reddit profiles
def redditor_info(file='',person=''):
    """ Function for analyzing through one or many redditors.
        Arguments(optional[text file], optional[[person]])
        You must enter 1 argument.
    """

    # Storing all headers for the csv file in one variable
    headlines = ['Name','Creation time','Redittor id','Is mod?','Is premium?','Comment karma','Link karma',
    'Verified email?','Reddit employee?']

    #Checking if both arguments are empty
    if file == '' and person == '':
        print("Please run the function with at least 1 argument.")
        return

    # If only file is empty then do a serach for the submitted profile
    elif file == '':

        # Opening csv file to store in redditor information
        with open('redditor.csv','w',newline='') as file:
            user = reddit.redditor(person)
            old = time.ctime(user.created_utc)
            writer = csv.DictWriter(file,fieldnames=headlines)
            writer.writeheader()
            writer.writerow({'Name': user.name,'Creation time': old,'Redittor id': user.id,'Is mod?': user.is_mod,'Is premium?': user.is_gold,
                            'Comment karma': user.comment_karma,'Link karma': user.link_karma,'Verified email?': user.has_verified_email,
                            'Reddit employee?': user.is_employee})


    else:
        try:
            f = open(file)
            whole_file = f.read()
            users = whole_file.split()

            #Opening csv file tot store information about redditors
            with open('redditors.csv','w',newline='') as file:
                writer = csv.DictWriter(file,fieldnames=headlines)
                writer.writeheader()

                #Iterating through every redditor
                for name in users:
                    user = reddit.redditor(name)
                    old = time.ctime(user.created_utc)
                    writer.writerow({'Name': user.name,'Creation time': old,'Redittor id': user.id,'Is mod?': user.is_mod,'Is premium?': user.is_gold,
                                    'Comment karma': user.comment_karma,'Link karma': user.link_karma,'Verified email?': user.has_verified_email,
                                    'Reddit employee?': user.is_employee})

        # Handling if the user enters non-existing file
        except OSError:
            print("Please type in correct file with reddit usernames.")
