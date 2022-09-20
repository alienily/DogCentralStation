"""
Code follows the CS340-demo-flask-app created by @mlapresta, @gkochera and @currym-osu
https://github.com/osu-cs340-ecampus/flask-starter-app
"""
# To actually have your app use this file, you need to RENAME the file to db_credentials.py
# You will find details about your CS340 database credentials on Canvas.

# the following will be used by the webapp.py to interact with the database
# You can also use environment variables

# For Local Devlelopment
host = 'localhost'
user = 'root'                                   # can be different if you set up another username in your MySQL installation
passwd = 'nottellingyou'                        # set accordingly
db = 'bsg'


# For OSU Flip Servers

# host = 'classmysql.engr.oregonstate.edu'      # MUST BE THIS
# user = '<your-cs-340-db-username-here>'       # don't forget the CS_340 prefix
# passwd = '<your-password-here>'               # should only be 4 digits if default
# db = '<name-of-database-on-osu-server>'                                  