# Reddit-Chat-Bot
Reddit bot that can post, reply, and comment with auto generated responses created for a class election campaign.

Note: Must have the latest version of praw installed. To install, use:
pip3 install praw 
or
pip install praw

Note: The praw.ini file must be set up correctly to function. Also, to create a bot use the bot_daemon function.
WARNING: This function intentionally uses an infinite loop, and once called, posts will be made every 60 seconds until the program is terminated.