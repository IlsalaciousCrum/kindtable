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

## Thing I've learned on this project:
+ The benefits of project managements, project design, carefully thinlking out your sprint goals.
+ The many benefits of daily standup (the effect on productivity of 
already knowing what you are going to do that day, checking in with timelines and goals everyday and how that keeps me on task)
+ Database migration. HB didn't seem to discuss that.
+ 