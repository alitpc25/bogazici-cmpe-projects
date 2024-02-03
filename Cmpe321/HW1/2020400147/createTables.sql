CREATE TABLE Users (
	username VARCHAR UNIQUE NOT NULL,
	password VARCHAR NOT NULL,
	name VARCHAR NOT NULL,
	surname VARCHAR NOT NULL,
	PRIMARY KEY (username)
);

CREATE TABLE Audience (
	username VARCHAR UNIQUE NOT NULL,
	PRIMARY KEY (username),
	FOREIGN KEY (username)
      REFERENCES Users
	ON DELETE CASCADE
	ON UPDATE CASCADE
	-- If it is deleted in Users table, cascade.
);

CREATE TABLE RatingPlatform (
	platform_id INT UNIQUE NOT NULL,
	platform_name VARCHAR UNIQUE NOT NULL,
	PRIMARY KEY (platform_id)
);

CREATE TABLE Director (
	username VARCHAR UNIQUE NOT NULL,
	nation VARCHAR NOT NULL,
	platform_id INT,
	PRIMARY KEY (username),
	FOREIGN KEY (username)
      REFERENCES Users
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	-- If it is deleted in Users table, cascade.
	FOREIGN KEY (platform_id)
      REFERENCES RatingPlatform
	ON DELETE NO ACTION
	-- Before deleting a rating platform, end the agreements.
);

CREATE TABLE DatabaseManagers (
	username VARCHAR UNIQUE NOT NULL,
	password VARCHAR NOT NULL,
	PRIMARY KEY (username)
);

CREATE TABLE RatingPlatformSubscriptions (
	username VARCHAR NOT NULL,
	platform_id INT NOT NULL,
	PRIMARY KEY (username, platform_id),
	FOREIGN KEY (username)
      REFERENCES Audience
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	-- If an audience is deleted, delete all of its subscriptions.
	FOREIGN KEY (platform_id)
      REFERENCES RatingPlatform
	ON DELETE CASCADE
	ON UPDATE CASCADE
	-- If the platform is deleted, delete all of its subscriptions.
);

CREATE TABLE Movies (
	movie_id INT UNIQUE NOT NULL,
	movie_name VARCHAR UNIQUE NOT NULL,
	duration INT NOT NULL,
	avg_rating FLOAT,
	director_username VARCHAR NOT NULL,
	PRIMARY KEY (movie_id),
	FOREIGN KEY (director_username) 
	REFERENCES Director(username)
	ON DELETE CASCADE
	-- If the director is deleted, delete all of his/her movies.
);

CREATE TABLE MovieRatings (
	username VARCHAR NOT NULL,
	movie_id INT NOT NULL,
	rating FLOAT CHECK (rating > 0 and rating <= 5) NOT NULL,
	PRIMARY KEY (username, movie_id),
	FOREIGN KEY (username)
      REFERENCES Audience,
	FOREIGN KEY (movie_id)
      REFERENCES Movies
	  ON DELETE CASCADE
	-- If the movie is deleted, delete all of its ratings.
);

CREATE TABLE Genre (
	genre_id INT UNIQUE NOT NULL,
	genre_name VARCHAR UNIQUE NOT NULL,
	PRIMARY KEY (genre_id)
);

CREATE TABLE MovieTypes (
	movie_id INT NOT NULL,
	genre_id INT NOT NULL,
	PRIMARY KEY (movie_id, genre_id),
	FOREIGN KEY (genre_id)
      REFERENCES Genre,
	FOREIGN KEY (movie_id)
      REFERENCES Movies
);

CREATE TABLE MovieSeries (
	movie_id INT NOT NULL,
	predecessor_movie_id INT NOT NULL,
	PRIMARY KEY (movie_id, predecessor_movie_id),
	FOREIGN KEY (movie_id)
      REFERENCES Movies,
	FOREIGN KEY (predecessor_movie_id)
      REFERENCES Movies
);

CREATE TABLE Theatre (
	theatre_id INT UNIQUE NOT NULL,
	theatre_name VARCHAR UNIQUE NOT NULL,
	theatre_district VARCHAR NOT NULL,
	theatre_capacity INT NOT NULL,
	PRIMARY KEY (theatre_id)
);

CREATE TABLE MovieSessions (
	session_id INT UNIQUE NOT NULL,
	movie_id INT NOT NULL,
	theatre_id INT NOT NULL,
	time_slot INT NOT NULL,
	date VARCHAR NOT NULL,
	PRIMARY KEY (theatre_id, time_slot, date),
	FOREIGN KEY (movie_id)
      REFERENCES Movies,
	FOREIGN KEY (theatre_id)
      REFERENCES Theatre,
	CONSTRAINT check_slot CHECK (time_slot IN (1, 2, 3, 4))
	-- Time slots can be 1, 2, 3 or 4.
);

CREATE TABLE TicketsSold (
	username VARCHAR NOT NULL,
	session_id INT NOT NULL,
	movie_id INT NOT NULL,
	theatre_id INT NOT NULL,
	time_slot INT NOT NULL,
	date VARCHAR NOT NULL,
	PRIMARY KEY (username, session_id),
	FOREIGN KEY (username)
      REFERENCES Audience,
	FOREIGN KEY (theatre_id, time_slot, date)
      REFERENCES MovieSessions
);