from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Lista de videojuegos
games = [
    {"title": "The Witcher 3", "genre": "RPG", "year": 2015, "size": "35 GB", "price": "$39.99", "image": "witcher3.jpg"},
    {"title": "Cyberpunk 2077", "genre": "RPG", "year": 2020, "size": "70 GB", "price": "$59.99", "image": "cyberpunk2077.jpg"},
    {"title": "Hades", "genre": "Action", "year": 2020, "size": "15 GB", "price": "$24.99", "image": "hades.jpg"},
    {"title": "Among Us", "genre": "Party", "year": 2018, "size": "0.5 GB", "price": "$4.99", "image": "amongus.jpg"},
    {"title": "Red Dead Redemption 2", "genre": "Adventure", "year": 2018, "size": "105 GB", "price": "$59.99", "image": "rdr2.jpg"},
    {"title": "Sekiro: Shadows Die Twice", "genre": "Action", "year": 2019, "size": "25 GB", "price": "$49.99", "image": "sekiro.jpg"},
    {"title": "Minecraft", "genre": "Sandbox", "year": 2011, "size": "1 GB", "price": "$26.95", "image": "minecraft.jpg"},
    {"title": "Fortnite", "genre": "Battle Royale", "year": 2017, "size": "30 GB", "price": "Free", "image": "fortnite.jpg"},
    {"title": "Resident Evil Village", "genre": "Horror", "year": 2021, "size": "45 GB", "price": "$59.99", "image": "residentevilvillage.jpg"},
    {"title": "God of War", "genre": "Action", "year": 2018, "size": "50 GB", "price": "$49.99", "image": "godofwar.jpg"},
    {"title": "The Legend of Zelda: Breath of the Wild", "genre": "Adventure", "year": 2017, "size": "13 GB", "price": "$59.99", "image": "botw.jpg"},
    {"title": "Hollow Knight", "genre": "Platformer", "year": 2017, "size": "9 GB", "price": "$14.99", "image": "hollowknight.jpg"},
    {"title": "Genshin Impact", "genre": "RPG", "year": 2020, "size": "30 GB", "price": "Free", "image": "genshinimpact.jpg"},
    {"title": "FIFA 22", "genre": "Sports", "year": 2021, "size": "50 GB", "price": "$59.99", "image": "fifa22.jpg"},
    {"title": "Call of Duty: Warzone", "genre": "Battle Royale", "year": 2020, "size": "80 GB", "price": "Free", "image": "warzone.jpg"},
    {"title": "Stardew Valley", "genre": "Simulation", "year": 2016, "size": "0.5 GB", "price": "$14.99", "image": "stardewvalley.jpg"},
    {"title": "Celeste", "genre": "Platformer", "year": 2018, "size": "1 GB", "price": "$19.99", "image": "celeste.jpg"},
    {"title": "DOOM Eternal", "genre": "FPS", "year": 2020, "size": "50 GB", "price": "$59.99", "image": "doometernal.jpg"},
    {"title": "Final Fantasy VII Remake", "genre": "RPG", "year": 2020, "size": "100 GB", "price": "$59.99", "image": "ff7remake.jpg"},
    {"title": "Super Mario Odyssey", "genre": "Platformer", "year": 2017, "size": "5.7 GB", "price": "$59.99", "image": "marioodyssey.jpg"},
    
    # Nuevos juegos añadidos
    {"title": "Assassin's Creed Valhalla", "genre": "Action", "year": 2020, "size": "90 GB", "price": "$59.99", "image": "acvalhalla.jpg"},
    {"title": "Ghost of Tsushima", "genre": "Action", "year": 2020, "size": "50 GB", "price": "$59.99", "image": "ghostoftsushima.jpg"},
    {"title": "Spider-Man: Miles Morales", "genre": "Action", "year": 2020, "size": "40 GB", "price": "$49.99", "image": "spiderman.jpg"},
    {"title": "Apex Legends", "genre": "Battle Royale", "year": 2019, "size": "30 GB", "price": "Free", "image": "apexlegends.jpg"},
    {"title": "Valorant", "genre": "FPS", "year": 2020, "size": "10 GB", "price": "Free", "image": "valorant.jpg"},
    {"title": "The Last of Us Part II", "genre": "Adventure", "year": 2020, "size": "100 GB", "price": "$59.99", "image": "tlou2.jpg"},
    {"title": "Fall Guys: Ultimate Knockout", "genre": "Party", "year": 2020, "size": "7 GB", "price": "$19.99", "image": "fallguys.jpg"},
    {"title": "Overwatch", "genre": "FPS", "year": 2016, "size": "30 GB", "price": "$39.99", "image": "overwatch.jpg"},
    {"title": "Dead by Daylight", "genre": "Horror", "year": 2016, "size": "15 GB", "price": "$19.99", "image": "deadbydaylight.jpg"},
    {"title": "Forza Horizon 5", "genre": "Racing", "year": 2021, "size": "100 GB", "price": "$59.99", "image": "forzahorizon5.jpg"},
    {"title": "League of Legends", "genre": "MOBA", "year": 2009, "size": "15 GB", "price": "Free", "image": "leagueoflegends.jpg"},
    {"title": "Dota 2", "genre": "MOBA", "year": 2013, "size": "15 GB", "price": "Free", "image": "dota2.jpg"},
    {"title": "Dark Souls III", "genre": "Action", "year": 2016, "size": "25 GB", "price": "$59.99", "image": "darksouls3.jpg"},
    {"title": "Persona 5 Royal", "genre": "RPG", "year": 2019, "size": "30 GB", "price": "$59.99", "image": "persona5.jpg"},
    {"title": "Nier: Automata", "genre": "Action", "year": 2017, "size": "50 GB", "price": "$39.99", "image": "nierautomata.jpg"}
]


# Simulación de base de datos de usuarios
users = [
    {"email": "user@example.com", "password": "1234"},
]

@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.form.get('search')
    selected_genre = request.form.get('genre')
    selected_year = request.form.get('year')
    selected_size = request.form.get('size')

    filtered_games = games

    if search_query:
        filtered_games = [game for game in games if search_query.lower() in game["title"].lower()]
    if selected_genre:
        filtered_games = [game for game in filtered_games if game["genre"] == selected_genre]
    if selected_year:
        filtered_games = [game for game in filtered_games if str(game["year"]) == selected_year]
    if selected_size:
        filtered_games = [game for game in filtered_games if game["size"] == selected_size]

    return render_template('index.html', games=filtered_games)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['logged_in'] = True
                flash('Inicio de sesión exitoso!', 'success')
                return redirect(url_for('home'))
        flash('Credenciales inválidas, intente de nuevo.', 'error')
    return render_template('login.html')

@app.route('/buy/<game_title>')
def buy(game_title):
    if not session.get('logged_in'):
        flash('Debes iniciar sesión para comprar.', 'warning')
        return redirect(url_for('login'))
    flash(f'Has comprado {game_title} con éxito!', 'success')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('Has cerrado sesión con éxito.', 'info')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
