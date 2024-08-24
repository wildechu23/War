import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def add_achievements():
    db = get_db()

    from .game import AchievementDescriptions
    for key, value in AchievementDescriptions.items():
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
    
    return db.execute(
        'SELECT * FROM UserAchievements WHERE UserID = ?', (user,)
    ).fetchall()


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


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)