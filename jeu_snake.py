import turtle
import time
import random
import sqlite3

delay = 0.1
score = 0
high_score = 0

# Connexion à la base de données (créée si elle n'existe pas)
conn = sqlite3.connect('snake_game.db')
c = conn.cursor()

# Création de la table des scores si elle n'existe pas
c.execute('''CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, high_score INTEGER)''')

# Récupération du meilleur score
c.execute('''SELECT high_score FROM scores WHERE id = 1''')
row = c.fetchone()
if row:
    high_score = row[0]
else:
    high_score = 0
    c.execute('''INSERT INTO scores (id, high_score) VALUES (1, 0)''')
    conn.commit()
    
# Fonction pour mettre à jour le meilleur score dans la base de données
def update_high_score(new_high_score):
    c.execute('''UPDATE scores SET high_score = ? WHERE id = 1''', (new_high_score,))
    conn.commit()
    
# Configuration de l'écran
wn = turtle.Screen()
wn.title("Jeu de Snake")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Éteint la mise à jour automatique de l'écran

# Tête du serpent
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Nourriture du serpent
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Tableau de bord
score_board = turtle.Turtle()
score_board.speed(0)
score_board.shape("square")
score_board.color("white")
score_board.penup()
score_board.hideturtle()
score_board.goto(0, 260)
score_board.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Dessiner la ligne de séparation
separator = turtle.Turtle()
separator.color("white")
separator.penup()
separator.hideturtle()
separator.goto(-300, 250)
separator.pendown()
separator.goto(300, 250)
separator.penup()

# Fonctions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def update_score_board():
    score_board.clear()
    score_board.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

def game_over():
    score_board.goto(0, 0)
    score_board.write("GAME OVER", align="center", font=("Courier", 40, "normal"))
    wn.update()
    time.sleep(2)
    score_board.clear()
    score_board.goto(0, 260)
    update_score_board()

# Clavier
wn.listen()
wn.onkeypress(go_up, "z")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "q")
wn.onkeypress(go_right, "d")

# Boucle principale du jeu
while True:
     # Logique du jeu, y compris la mise à jour du meilleur score si nécessaire
    if score > high_score:
        high_score = score
        update_high_score(high_score)
        
    wn.update()
    
    # Vérifier la collision avec la bordure
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>240 or head.ycor()<-290:
        game_over()
        head.goto(0,0)
        head.direction = "stop"
        
        # Cacher les segments
        for segment in segments:
            segment.goto(1000, 1000)
        
        # Effacer la liste des segments
        segments.clear()

        # Réinitialiser le score
        score = 0

    
    # Vérifier la collision avec la nourriture
    if head.distance(food) < 20:
        # Déplacer la nourriture à un endroit aléatoire
        x = random.randint(-12, 12)*20
        y = random.randint(-12, 12)*20
        food.goto(x, y)
        
        # Ajouter un segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)
        
        # Augmenter le score
        score += 10
        if score > high_score:
            high_score = score
        update_score_board()
    
    # Déplacer les segments en ordre inverse
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
        
    # Déplacer le segment 0 à l'endroit de la tête
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)
    
    move()
    
    # Vérifier la collision avec le corps
    for segment in segments:
        if segment.distance(head) < 20:
            game_over()
            head.goto(0,0)
            head.direction = "stop"
            
            # Cacher les segments
            for segment in segments:
                segment.goto(1000, 1000)
            
            # Effacer la liste des segments
            segments.clear()

            # Réinitialiser le score
            score = 0

    
    time.sleep(delay)

wn.mainloop()
