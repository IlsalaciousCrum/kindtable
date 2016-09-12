# Post Career Day Further Development

This is my public to-do list for my Hackbright Academy final project, Kind Table. All development thus far happened in two -- two-week-long sprints, while other things were going on. This web app is functional as is but there is so much that I wanted to add and learn. And refactor. :blush:

- [ ] Testing
    - [ ] Unittests [flask](http://flask.pocoo.org/docs/0.11/testing/)
    - [ ] SQLAlchemy tests
    - [ ] Mock server
- [ ] SQL Alchemy
    - [ ] In My Party Profile, a field to display date/time/location of planned party.
    - [ ] Refactor SQLAlchemy and functions so that it's the same function for user and guest
- [ ] Python
    - [ ] Fix recipe and ingredient storage - decoding and encoding UTF-8
    - [ ] Ability to change anything you have added, everywhere
    - [ ] for login page, blanks and other errors are currently handled by HTML coding. They should probably be handled on the server side with python
    - [ ] Logic for all forms to handle capitalization. store information in all lower caps, capitalize it as needed
    - [ ] Check all form logic for the ability to handle duplicates and correct
    - [ ] Python logic to handle claiming your account
    - [ ] On the user table, who owns the profile, only shows to who owns it
- [ ] Flask
    - [ ] [Understand the back code snippet and implement it](http://flask.pocoo.org/snippets/120/)
    - [ ] Can I refactor HTML with Jinja to capitalize on inheritance so that User profile, Friend profile and guest profile all use the same templates? So that the same templates are used in many places?
    - [ ] Change base template login/logout session handling to [official handling](http://flask.pocoo.org/docs/0.11/tutorial/templates/#layout-html). Remove from Flask Routes. I think using the conditionals you can just have a different template load
- [ ] Javascript
    - [ ] AJAX calls to make infinite scroll on recipe page
    - [ ] AJAX calls to rerun search on recipe search page
    - [ ] Angular JS for most responsive interface
- [ ] APIs
    - [ ] add emailing for lost passwords, connecting friends, beta-test codes
        - [Using flask](https://pythonhosted.org/flask-mail/)
        - [Using an email API](http://blog.mashape.com/list-of-10-email-apis/)

    - [ ] [easily preload your friends from your address book (Todd)](https://developers.google.com/people/v1/getting-started)
    - [ ] [connect facebook to load your friends (Javascript SDK)](https://developers.facebook.com/docs/facebook-login/permissions#reference-user_friends)
        - user_friends
        - Provides access the list of friends that also use your app. These friends can be found on the friends edge on the user object.
        - In order for a person to show up in one person's friend list, both people must have decided to share their list of friends with your app and not disabled that permission during login.Also both friends must have been asked for user_friends during the login process.
        - user_friends


As of 9/11/16 5:00pm