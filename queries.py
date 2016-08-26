
###########################################################################

Views for testing that SQLAlchemy functions are working correctly


CREATE VIEW user_intolerances AS
SELECT users.user_id, users.username, intolerances.intol_name
FROM userintolerances
JOIN users ON users.user_id = userintolerances.user_id
JOIN intolerances ON userintolerances.intol_id = intolerances.intol_id
ORDER BY users.user_id;


CREATE VIEW partyavoids AS
SELECT partyguests.party_id, partyguests.title, partyguests.user_id, partyguests.username, user_avoidances.ingredient
FROM partyguests
# JOIN user_avoidances on partyguests.user_id = user_avoidances.user_id;

CREATE VIEW partydiets AS
SELECT partyguests.party_id, partyguests.title, partyguests.user_id, partyguests.username, user_diets.diet_type
FROM partyguests
JOIN user_diets on partyguests.user_id = user_diets.user_id;


CREATE VIEW partyintolerances AS
SELECT partyguests.party_id, partyguests.title, partyguests.user_id, partyguests.username, user_intolerances.intol_name
FROM partyguests
JOIN user_intolerances on partyguests.user_id = user_intolerances.user_id;



CREATE VIEW User_Diets AS SELECT user_id, username, diets.diet_type
FROM users
  JOIN diets
    ON users.diet_id = diets.diet_id
    ORDER BY user_id;


CREATE VIEW User_Intolerances AS SELECT user_id, username, diets.diet_type
FROM users
  JOIN diets
    ON users.diet_id = diets.diet_id
    ORDER BY user_id;



CREATE VIEW User_Diets AS SELECT user_id, username, diets.diet_type
FROM users
  JOIN diets
    ON users.diet_id = diets.diet_id
    ORDER BY user_id;

CREATE VIEW user_avoidances AS SELECT users.user_id, users.username, avoid.ingredient
FROM users
  JOIN avoid
    ON users.user_id = avoid.user_id
     ORDER BY users.user_id;


CREATE VIEW partyguests AS
SELECT parties.party_id, parties.title, users.user_id, users.username
FROM party_guests
JOIN users ON users.user_id = party_guests.user_id
JOIN parties ON parties.party_id = party_guests.party_id
ORDER BY parties.party_id;






############################################################################