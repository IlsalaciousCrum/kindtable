#### When something is completed, ~~cross it out~~.
#### When a question is answered, add the answer below it in *italics*.
#### If the thought wouldn't help someone understand your process, cross it out.


## Questions for an expert:
1. Since this is a show piece, is it better to do things the efficient way, ie using Flask Login to manage user authentication, WTF for form validation or 
is it better to code everything in Python to show my Python skills?
2. Is there a convention for string length for SQL/SQL Alchemy? I remember in HB that all of the examples had specific string lengths related to binary but it
is not required and examples from the internet don't conform to that.
3. When it is deployed, should it be a beta deployment and users need to email me? Seems silly but I want to feel safe having fields where users can write
themselves notes.


## To Do:

+ Update seed file to add a default user_id for the profiles table to use when there is not a registered user for that profile. Instead of a hashed password, store something that is not a hash and will never validate through user authentication so that no one can ever use that user_id to log in.
+ functions that add a date and time to the party: http://stackoverflow.com/questions/12019766/how-to-get-month-and-year-from-date-field-in-sqlalchemy
+ indicate when a profile was last updated - tells the user so they can determine if they want to refresh the information.
+ classmethod datetime.utcnow()
Return the current UTC date and time, with tzinfo None. This is like now(), but returns the current UTC date and time, as a naive datetime object. See also now().
+ POST/Redirect/Get for forms to eliminate the possibility of refreshing a post form.
+ url_for() gets passed the view function name (like 'show_login_form') and so will still work if you change the route name later. 
+ sending asynchronous email - Thread or Celery queue



## Thing I've learned on this project:
+ The benefits of project managements, project design, carefully thinlking out your sprint goals.
+ The many benefits of daily standup (the effect on productivity of 
already knowing what you are going to do that day, checking in with timelines and goals everyday and how that keeps me on task)
+ Database migration. HB didn't seem to discuss that.
+ When designing the model, discriminating between what is information to be stored or accessed through object oriented programming vs. queries

## Future Features:
+ being able to attach preferred recipes to a profile. So a user would get ideas of things to make for this friend
+ updating google calendar with dinner party dates and invites

