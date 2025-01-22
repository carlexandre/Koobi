# Koobi
## Video Demo:  <URL HERE>
## Description: 

#### Koobi is a website that works like a notepad, where you can make notes on various subjects, such as thoughts, venting, passwords, poems, stories and much more.

#### The project is divided into 3 folders (flask_session to save incoming users, static and templates), 2 python files (app.py and helpers.py) and a database (koobi.db).

## Database
> koobi.db: Database to store each user's data, such as their username and password in hashed form, the notes along with their title and the date they were made or modified.

### Tables created:
  
  - **TABLE** users(
    - id **INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL**
    - username **TEXT NOT NULL**
    - hash **TEXT NOT NULL**
  
  - **TABLE** notes(
    - id **INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL**
    - user_id **INTEGER NOT NULL**
    - title **TEXT**
    - note **TEXT**
    - date **TIMESTAMP**
    - **FOREIGN KEY** (user_id) **REFERENCES** users (id)

## Back-end

### helpers.py 
> This file only has the login_required(f) function to restrict the other areas from being accessed by people without a login.

### app.py
> This is the back-end of the entire website, using flask and the SQL function from the cs50 library to configure the pages and the code for each one. We use flask_session to find out which user is accessing the site. In this file we have 7 routes: “/”, “/login”, “/logout”, “/register”, “/newnote”, “/edit/<int:note_id>”, “/delete/<int:note_id>”. These will take you to Koobi's various functionalities.

 - #### “/” :
This is the homepage, where the notes will be stored, where we save the notes made by the user in a variable using ‘db.execute’ and send this information to the html (notes.html) with the render_template and also delete notes from the database that are repeated due to double-click bugs when sending the form. This page only uses the GET method.

- #### “/login":
If you haven't registered or logged in yet, this is the page you will go to. When the POST method is used, it checks that the username and password are correct. If the login is correct, it takes the user id from the database and puts it in the session to save the login. When the method is GET it just returns render_template with login.html

- #### “/register":
Similar to login, if the method is POST it will check if the username already exists, if the password is short or long. If this is the case, it will transform the password into a hash, a more secure form of password using the generate_password_hash function, and then it will hash both the username and the password in the database in the users table.

- #### “/logout":
Clears the session and returns it to ‘/’, but as there is no login, it is returned to ‘/login’ because of the login_required(f) function.

- #### “/newnote":
In the POST method, it takes the title, the text of the note, the id of the user who is making the note and the date along with the time and puts it into the database in the notes table. In the GET method, it returns the html along with the username to do the fulfillment.

- #### “/edit/<int:note_id.":
Here, as we need to know the id of each note that is being accessed, we use /<int:note_id> to get from the html the id that is being put in the action attribute of the form” and thus be able to modify it in the database by the POST method.

- #### “/delete/<int:nota_id>":
Similar to edit, it takes the id of the note to delete it.

## Front-end
> The front-end is in the static and templates folders.

### static
> This is where the css and javascript used, the images and favicons are.

- #### styles.css:
Here are the visual changes we made to the html, we used some bootstraps along with some individual changes. To make the site more responsive on other screens, we used @media only screen and (max-width: 768px), so there will be some changes for mobile screens and smaller devices.

- #### script.js:
Here you only have the Search() function, but there is also the use of javascript within the htmls themselves. This function is responsible for searching for notes and only displaying them. It takes the id of the input and the class of the eachnote div, which is responsible for each individual note. Using a forEach we can take the id of each note and put that id in a variable called idtitle so that we can take the title that has that same id as the value of the “data-title” attribute, then check if the text is in the input, if it is we remove the hidden class and if not we add it to eachnote.

### templates
> The htmls for all the pages are here, they are: layout.html, edit.html, login.html, newnote.html, notes.html, register.html

- #### layout.html:
This is the main html for all the pages, using jinja we can create blocks for other htmls to be inserted inside it. Here you have the navbar along with a jinja condition to show different links depending on whether the user is logged in or not.

- #### login.html/register.html:
Login and registration page, with a username and password form. We have a condition in jinja to show alerts with flask flash. In the script, we have 2 functions, one to make the alert disappear after 5 seconds, the other to make the password appear when you click on the closed padlock and make it disappear when you click on the open padlock.

- #### notes.html:
Html of the homepage, where the cards with the notes and titles will be. We used jinja again to separate each note individually using a for. We also made a button area to add a new note and an area that appears to make sure the person wants to delete it. We have 2 scripts in this html, one so that if the text is longer than 390 characters it will occupy 100% of the available width, the other to make the delete confirmation area appear and direct it to the route “/delete/<int:note-id>” with the id of the note you want to delete.

- #### newnote.html/edit.html:
Similar Html, as they have the same format for creating and modifying a note.