DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Achievements;
DROP TABLE IF EXISTS UserAchievements;


CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY,
    Username TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL
);

CREATE TABLE Achievements (
    AchievementID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Details TEXT
);

CREATE TABLE UserAchievements (
    UserAchievementID INTEGER PRIMARY KEY,
    UserID INTEGER NOT NULL,
    AchievementID INTEGER NOT NULL,
    UnlockedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (AchievementID) REFERENCES Achievements(AchievementID)
);