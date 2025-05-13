# Recipe-Maker
A simple Flask web app that allows users to share food recipes. 
Users can log in, create recipes, build a collection, and plan meals.

## Team 6
- Charlie (@c-banh-mi)
- Gabriel (@gmartins-11)
- Jayden (@AloofOddBall)

## Ethical Implications
When building a food recipe blog for our users, we must keep in mind the obligatory ethical and professional responsibilities 
developers have to ensure user trust, safety, and fairness. Developers must protect any sensitive and personal data by using 
secure storage and encryption practices, ensuring that users can safely engage with the platform. Furthermore, in the global context, 
users can come from diverse cultural backgrounds with different diets, so the hobby of sharing recipes should be inclusive and respectful, 
leaving no room for harmful stereotypes, exclusions, or bullying. Economically, our blog offers an open platform to promote free food education 
without creating financial barriers, supporting the sharing of knowledge among all users. Environmentally, our food blog being a lightweight 
website also reduces server energy consumption, supporting sustainable web development practices. From a societal perspective, our food blog 
promotes an open safe space of accessible recipes that can encourage healthier cooking habits and improve public health and wellbeing. 
We also have a responsibility to moderate content to prevent the spread of misinformation, such as unsafe cooking practices or false nutritional claims. 
In every decision, we must aim to create a platform that empowers individuals, promotes inclusivity, and upholds strong ethical standards in 
both technology and online communities.

## How to Get Started
1. clone the repository
2. create and activate a virtual environment
3. install the project dependencies
4. run
5. open web browser and go to http://127.0.0.1:5000/

```bash
$ git clone https://github.com/AloofOddBall/Recipe-Maker
$ cd Recipe-Maker
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ flask db init # ignore if already exists
$ flask db migrate -m "Initial migration"
$ flask db upgrade
$ flask run
```

## Functional Requirements
1. User Registration			Jayden
2. User Login				      Jayden
3. User Logout				    Jayden
4. Create Recipe			    Charlie
5. Edit Recipe				    Charlie
6. Delete Recipe			    Gabriel
7. View Recipe				    Gabriel
8. Search Recipe
9. Rate Recipe
10. Comment on Recipe
11. View User Profile
12. Edit User Profile 
13. Save Recipe (Favorite) 
14. View All Recipes
15. Filter Recipes
16. Delete Comments
17. Reply to Comments
18. Rate Comments

## GitHub Repository
https://github.com/AloofOddBall/Recipe-Maker
