import sqlite3

import click
from flask import current_app, g, session

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_user():
    user_id = session.get('user_id')

    if user_id:
        db = get_db()

        user = db.execute(
            'SELECT * FROM Users WHERE UserID = ?', 
            (user_id,)
        ).fetchone()

        return user

def get_user_profile(user_id):
    db = get_db()

    user = db.execute(
        'SELECT * FROM UserProfiles WHERE UserID = ?', 
        (user_id,)
    ).fetchone()

    return user

def update_profile(user_id, profile):
    db = get_db()

    try:
        db.execute(
            '''
                UPDATE UserProfiles
                SET (Wins, Losses, TotalKills, TotalAssists, Charges, Blocks) = (?, ?, ?, ?, ?, ?)
                WHERE UserID = ?
            ''',
            (
                profile['Wins'], 
                profile['Losses'], 
                profile['Total Kills'], 
                profile['Total Assists'], 
                profile['Charges Acquired'],
                profile['Blocks Acquired'],
                user_id
            )
        )
        db.commit()
    except:
        print("Error on update user " + user_id)
    
def get_username(id):
    db = get_db()
    print(id)
    username = db.execute(
        'SELECT Username FROM Users WHERE UserID = ?', 
        (id,)
    ).fetchone()
    
    return username[0] if username else None

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_achievements():
    db = get_db()

    try:
        db.execute(
            "DROP TABLE IF EXISTS Achievements",
        )
        db.commit()

        db.execute('''
            CREATE TABLE Achievements (
                AchievementID INTEGER PRIMARY KEY,
                Title TEXT NOT NULL,
                Details TEXT
            );
        ''',
        )
        db.commit()
    except:
        print("Error on creating Achievements")

def add_achievements():
    db = get_db()


    from .game import getAchievementDescriptions
    for key, value in getAchievementDescriptions().items():
        try:
            db.execute(
                "INSERT INTO Achievements (Title, Details) VALUES (?, ?)",
                (key, value),
            )
            db.commit()
        except:
            print("Error on inserting Achievement " + key)

def unlock_achievement(user, title):
    db = get_db()

    print(title)
    achievement = db.execute(
        'SELECT * FROM Achievements WHERE Title = ?', (title,)
    ).fetchone()

    if achievement is None:
        print("Achievement not found")
        return

    print(user, "has unlocked the achievement", title, ": " + achievement['Details'])

    try:
        db.execute(
            "INSERT INTO UserAchievements (UserID, AchievementID) VALUES (?, ?)",
            (user, achievement['AchievementID'])
        )
        db.commit()
    except:
        print("Failed to unlock achievement")

def get_achievements(user):
    db = get_db()
    
    return db.execute('''
        SELECT a.AchievementID,
               a.Title,
               a.Details, 
               CASE 
                   WHEN ua.UserID IS NOT NULL THEN 1 
                   ELSE 0 
               END AS HasAchievement
        FROM Achievements a
        LEFT JOIN UserAchievements ua
        ON a.AchievementID = ua.AchievementID 
        AND ua.UserID = ?
    ''', (user,)).fetchall()
    


def get_missing_achievements(user):
    db = get_db()
    
    return db.execute('''
        SELECT a.*
        FROM Achievements a
        LEFT JOIN UserAchievements ua
        ON a.AchievementID = ua.AchievementID
        AND ua.UserID = ?
        WHERE ua.UserID IS NULL
    ''', (user,)).fetchall()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    add_achievements()
    click.echo('Initialized the database.')

@click.command('add-db')
def add_db_command():
    init_achievements()
    add_achievements()
    click.echo('Added Achievements')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_db_command)