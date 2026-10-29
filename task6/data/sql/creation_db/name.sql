CREATE TABLE first_name (
    first_name_id SERIAL,
    locale_id SMALLINT NOT NULL,
    value VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    CONSTRAINT PK_first_name_first_name_id PRIMARY KEY (first_name_id),
    CONSTRAINT FK_first_name_locale_id FOREIGN KEY (locale_id) REFERENCES locale (locale_id),
    CONSTRAINT CHK_first_name_gender CHECK (gender IN ('F', 'M')),
	CONSTRAINT UNQ_first_name_locale_value_gender UNIQUE (locale_id, value, gender)
);

CREATE TABLE last_name (
    last_name_id SERIAL,
    locale_id SMALLINT NOT NULL,
    value VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    CONSTRAINT PK_last_name_last_name_id PRIMARY KEY (last_name_id),
    CONSTRAINT FK_last_name_locale_id FOREIGN KEY (locale_id) REFERENCES locale (locale_id),
    CONSTRAINT CHK_last_name_gender CHECK (gender IN ('F', 'M')),
	CONSTRAINT UNQ_last_name_locale_value_gender UNIQUE (locale_id, value, gender)
);

CREATE TABLE title (
    title_id SMALLSERIAL,
    locale_id SMALLINT NOT NULL,
    value VARCHAR(20) NOT NULL,
    gender CHAR(1) NOT NULL,
    CONSTRAINT PK_title_title_id PRIMARY KEY (title_id),
    CONSTRAINT FK_title_locale_id FOREIGN KEY (locale_id) REFERENCES locale (locale_id),
    CONSTRAINT CHK_title_gender CHECK (gender IN ('F', 'M')),
    CONSTRAINT UNQ_title_locale_value_gender UNIQUE (locale_id, value, gender)
);

INSERT INTO title (locale_id, value, gender)
VALUES
    (1, 'Mr.', 'M'),
    (1, 'Mrs.', 'F'),
    (1, 'Ms.', 'F'),
    (1, 'Miss', 'F'),
    (1, 'Mx.', 'M'),
    (1, 'Mx.', 'F'),
    (1, 'Dr.', 'M'),
    (1, 'Dr.', 'F'),
    (1, 'Prof.', 'M'),
    (1, 'Prof.', 'F'),
    (1, 'Rev.', 'M'),
    (1, 'Rev.', 'F'),
    (1, 'Capt.', 'M'),
    (1, 'Capt.', 'F'),
    (1, 'Col.', 'M'),
    (1, 'Col.', 'F'),
    (1, 'Major', 'M'),
    (1, 'Major', 'F'),
    (1, 'General', 'M'),
    (1, 'General', 'F'),
    (1, 'Admiral', 'M'),
    (1, 'Admiral', 'F'),
    (1, 'Judge', 'M'),
    (1, 'Judge', 'F'),
    (1, 'Rabbi', 'M'),
    (1, 'Rabbi', 'F'),
    (1, 'Father', 'M'),
    (1, 'Sister', 'F'),
    (2, 'Pan', 'M'),
    (2, 'Pani', 'F'),
    (2, 'Dr.', 'M'),
    (2, 'Dr.', 'F'),
    (2, 'Prof.', 'M'),
    (2, 'Prof.', 'F'),
    (2, 'Ks.', 'M'),
    (2, 'Siostra', 'F'),
	(2, 'gen.', 'M'),
    (2, 'gen.', 'F'),
    (2, 'adm.', 'M'),
    (2, 'adm.', 'F'),
    (2, 'płk', 'M'),
    (2, 'płk', 'F'),
    (2, 'mjr', 'M'),
    (2, 'mjr', 'F'),
    (2, 'kpt.', 'M'),
    (2, 'kpt.', 'F');

CREATE TABLE name_suffix (
    name_suffix_id SMALLSERIAL,
    locale_id SMALLINT NOT NULL,
    value VARCHAR(10) NOT NULL,
	gender CHAR(1) NOT NULL,
    CONSTRAINT PK_name_suffix_name_suffix_id PRIMARY KEY (name_suffix_id),
    CONSTRAINT FK_name_suffix_locale_id FOREIGN KEY (locale_id) REFERENCES locale (locale_id),
	CONSTRAINT CHK_name_suffix_gender CHECK (gender IN ('F', 'M')),
    CONSTRAINT UNQ_name_suffix_locale_value_gender UNIQUE (locale_id, value, gender)
);

INSERT INTO name_suffix (locale_id, value, gender)
VALUES
    (1, 'Jr.', 'F'),
    (1, 'Sr.', 'F'),
    (1, 'II', 'F'),
    (1, 'III', 'F'),
    (1, 'IV', 'F'),
    (1, 'V', 'F'),
	(1, 'Jr.', 'M'),
    (1, 'Sr.', 'M'),
    (1, 'II', 'M'),
    (1, 'III', 'M'),
    (1, 'IV', 'M'),
    (1, 'V', 'M'),
	(2, 'II', 'F'),
    (2, 'III', 'F'),
    (2, 'IV', 'F'),
    (2, 'V', 'F'),
	(2, 'II', 'M'),
    (2, 'III', 'M'),
    (2, 'IV', 'M'),
    (2, 'V', 'M');
