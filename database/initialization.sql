CREATE DATABASE summertime_practice_t;
\c summertime_practice_t;
CREATE TABLE vacancies (
vacancy_name VARCHAR(100),
vacancy_url VARCHAR(300) PRIMARY KEY,
company VARCHAR(100),
area VARCHAR(50),
education VARCHAR(100),
salary VARCHAR(100),
experience VARCHAR(100),
employment VARCHAR(100),
description TEXT,
key_skills TEXT);