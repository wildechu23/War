DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Achievements;
DROP TABLE IF EXISTS UserAchievements;


CREATE TABLE Users (
    UserId INTEGER PRIMARY KEY,
    Username TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL
);

CREATE TABLE Achievements (
    AchievementId INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Details TEXT,
);

CREATE TABLE UserAchievements (
    UserAchievementId INTEGER PRIMARY KEY,
    UserId INTEGER NOT NULL,
    AchievementId INTEGER NOT NULL,
    UnlockedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (AchievementID) REFERENCES Achievements(AchievementID)
);