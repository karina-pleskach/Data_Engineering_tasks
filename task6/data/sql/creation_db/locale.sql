DROP TABLE IF EXISTS locale;

CREATE TABLE locale (
    locale_id SMALLSERIAL,
    language_code CHAR(2) NOT NULL,
    country_code CHAR(2) NOT NULL,
    name VARCHAR(50) NOT NULL,
    CONSTRAINT PK_locale_locale_id PRIMARY KEY (locale_id),
    CONSTRAINT UNQ_locale_language_country UNIQUE (language_code, country_code),
    CONSTRAINT CHK_locale_language_code CHECK (language_code ~ '^[a-z]{2}$'),
    CONSTRAINT CHK_locale_country_code CHECK (country_code ~ '^[A-Z]{2}$')
);

INSERT INTO locale (language_code, country_code, name)
VALUES
    ('en', 'US', 'English/USA'),
    ('pl', 'PL', 'Polish/Poland');
