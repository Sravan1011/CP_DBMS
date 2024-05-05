from flask import Flask, render_template, request, redirect, url_for
import MySQLdb
import MySQLdb.cursors
from flask import flash

app = Flask(__name__)
app.secret_key = '1011'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sravan11!'
app.config['MYSQL_DB'] = 'courseproject'


mysql = MySQLdb.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        password=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'],
                        cursorclass=MySQLdb.cursors.DictCursor)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        cursor = mysql.cursor()
        cursor.execute("SELECT cuisine_id, cuisine_name FROM cuisine1")
        cuisines = cursor.fetchall()
        return render_template('home.html', cuisines=cuisines)  
    if request.method == "POST":
        cuisine_name = request.form['cuisine']
        recipe_name = request.form['recipe_name']
        meal_type = request.form['meal_type']
        category = request.form['category']
        procedure = request.form['procedure']
        ingredients = request.form['ingredients']
        cursor = mysql.cursor()

        cursor.execute("SELECT cuisine_id FROM cuisine1 WHERE cuisine_name = %s", (cuisine_name,))
        result = cursor.fetchone()
        if result:
            cuisine_id = result['cuisine_id']
        else:
            
            return 'Cuisine not found'
        cursor.execute("SELECT MealType_ID FROM MealType WHERE TypeName = %s", (meal_type,))
        result = cursor.fetchone()
        if result:
            meal_type_id = result['MealType_ID']
        else:
            
            return 'Meal type not found'

        
        cursor.execute("SELECT CategoryID FROM Category WHERE Category_name = %s", (category,))
        result = cursor.fetchone()
        if result:
            category_id = result['CategoryID']
        else:
            
            return 'Category not found'

        
        cursor.execute("SELECT MAX(RecipeID) AS max_recipe_id FROM Recipe")
        max_recipe_id_result = cursor.fetchone()
        if max_recipe_id_result and max_recipe_id_result['max_recipe_id'] is not None:
            max_recipe_id = max_recipe_id_result['max_recipe_id']
        else:
            max_recipe_id = 0

        
        new_recipe_id = max_recipe_id + 1

        
        cursor.execute("""
            INSERT INTO Recipe (RecipeID, CuisineID, RecipeName, MealTypeID, CategoryID, Steps, Ingredients)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (new_recipe_id, cuisine_id, recipe_name, meal_type_id, category_id, procedure, ingredients))

        mysql.commit()
        return redirect(url_for('recipe_added'))


@app.route('/recipeAdded', methods=["GET", "POST"])
def recipe_added():
    return 'Recipe added successfully'


@app.route('/recipes', methods=["GET"])
def view_recipes():
    cursor = mysql.cursor()

    
    cursor.execute("SELECT cuisine_id, cuisine_name FROM cuisine1")
    cuisines = cursor.fetchall()

    return render_template('index.html', cuisines=cuisines)


@app.route('/recipes/<cuisine_id>', methods=["GET"])
def recipes(cuisine_id):
    cursor = mysql.cursor()

    
    cursor.execute("SELECT cuisine_name FROM cuisine1 WHERE cuisine_id = %s", (cuisine_id,))
    result = cursor.fetchone()
    if result:
        cuisine_name = result['cuisine_name']
    else:
      
        return 'Cuisine not found'

    
    cursor.execute("SELECT RecipeID, RecipeName, Calories FROM Recipe WHERE CuisineID = %s", (cuisine_id,))
    recipes = cursor.fetchall()

    
    for recipe in recipes:
        recipe_id = recipe['RecipeID']
        cursor.execute("SELECT AVG(rating) AS avg_rating FROM reviews WHERE recipe_id = %s", (recipe_id,))
        avg_rating_result = cursor.fetchone()
        avg_rating = avg_rating_result['avg_rating'] if avg_rating_result['avg_rating'] else 0
        recipe['avg_rating'] = avg_rating
        
      

    return render_template('recipes.html', recipes=recipes, cuisine_id=cuisine_id, cuisine_name=cuisine_name)


@app.route('/recipes/<cuisine_id>/<recipe_id>', methods=["GET"])
def recipe_details(cuisine_id, recipe_id):
    cursor = mysql.cursor()

    
    cursor.execute("SELECT RecipeName, Calories, Ingredients, MacroNutrients, Steps FROM Recipe WHERE RecipeID = %s AND CuisineID = %s",
                   (recipe_id, cuisine_id))
    recipe = cursor.fetchone()

    return render_template('recipe_details.html', recipe=recipe, recipe_id=recipe_id,cuisine_id=cuisine_id)

@app.route('/chefs', methods=["GET"])
def chefs():
    cursor = mysql.cursor()
    cursor.execute("SELECT DISTINCT chef_id, chef_name,image_url FROM chefs")

    chefs = cursor.fetchall()
    return render_template('chefs.html', chefs=chefs)

@app.route('/chefs/<int:chef_id>/recipes', methods=["GET"])
def chef_recipes(chef_id):
    cursor = mysql.cursor()
    cursor.execute("SELECT recipe_id, recipe_name FROM chef_recipes WHERE chef_id = %s", (chef_id,))
    recipes = cursor.fetchall()
    return render_template('chef_recipes.html', recipes=recipes, chef_id=chef_id)



@app.route('/chefs/<int:chef_id>/recipes/<int:recipe_id>', methods=["GET"])
def chef_recipe_details(chef_id, recipe_id):
    cursor = mysql.cursor()

    
    cursor.execute("SELECT * FROM recipe_details WHERE chef_id = %s AND recipe_id = %s", (chef_id, recipe_id))


    recipe_details = cursor.fetchone()

    if recipe_details:
        return render_template('chef_recipe_details.html', recipe_details=recipe_details)
    else:
        return 'Recipe not found for this chef'

    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = int(request.form['age'])  
        try:
             
            cursor = mysql.cursor()
            cursor.execute("INSERT INTO users (username, password, age) VALUES (%s, %s, %s)", (username, password, age))
            mysql.commit()
            flash("Signup successful. Please log in.", 'success')
            return redirect(url_for('login'))  
        except MySQLdb.MySQLError as err:
            flash("An error occurred: " + str(err), 'danger')  
            return redirect(url_for('signup'))  

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        if user:
           
            flash("Login successful.", 'success')
            return redirect(url_for('index'))  
        else:
           
            flash("Incorrect username or password.", 'danger')
            return redirect(url_for('login')) 

    return render_template('login.html')

@app.route('/recipes/<int:recipe_id>/reviews', methods=['GET', 'POST'])
def add_review(recipe_id):
   
    cuisine_id = request.form['cuisine_id']
    if request.method == 'POST':
        user_id = request.form.get('user_id', None)  
        rating = request.form['rating']
        comment = request.form['comment']

        cursor = mysql.cursor()
        cursor.execute("""
            INSERT INTO reviews (recipe_id, user_id, rating, comment)
            VALUES (%s, %s, %s, %s)
        """, (recipe_id, user_id, rating, comment))
        mysql.commit()

    return redirect(url_for('recipe_details', cuisine_id=cuisine_id, recipe_id=recipe_id))





    





if __name__ == '__main__':
    app.run(debug=True)
