CREATE TABLE users_address (
    id           SERIAL      PRIMARY KEY,
    user_address VARCHAR (20) UNIQUE
);

CREATE TABLE users_phone (
    id           SERIAL      PRIMARY KEY,
    user_phone VARCHAR (11) UNIQUE
);

CREATE TABLE users_name (
    id           SERIAL      PRIMARY KEY,
    user_name VARCHAR (30) UNIQUE
);

CREATE TABLE users_surname (
    id           SERIAL      PRIMARY KEY,
    users_surname VARCHAR (30) UNIQUE
);

CREATE TABLE users_lastname (
    id           SERIAL      PRIMARY KEY,
    users_lastname VARCHAR (20) UNIQUE
);

CREATE TABLE full_info_user (
    id       SERIAL PRIMARY KEY,
    user_name     INTEGER REFERENCES users_name (id) ON DELETE CASCADE
                                               ON UPDATE CASCADE,
    surname  INTEGER REFERENCES users_surname (id) ON DELETE CASCADE
                                             ON UPDATE CASCADE,
	lastname INTEGER REFERENCES users_lastname (id) ON DELETE CASCADE
                                              ON UPDATE CASCADE,
    address  INTEGER REFERENCES users_address (id) ON DELETE CASCADE
                                                 ON UPDATE CASCADE,
    phone    INTEGER REFERENCES users_phone (id) ON DELETE CASCADE
                                                ON UPDATE CASCADE
);

