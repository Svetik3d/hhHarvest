import psycopg2
import data_models
import save_data_to_file


# Конфигурация базы данных
db_config = {
    'dbname': 'summertime_practice',
    'user': 'postgres',
    'password': 'пароль',
    'host': '',
    'port': '5432'
}

def init_t():
    with psycopg2.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS vacancies (
vacancy_name VARCHAR(500),
vacancy_url VARCHAR(500) PRIMARY KEY,
company VARCHAR(100),
area VARCHAR(200),
education VARCHAR(200),
salary VARCHAR(100),
experience VARCHAR(100),
employment VARCHAR(100),
description TEXT,
key_skills TEXT);"""
        cursor.execute(query)

def save_all_data(datas):
    urls = get_urls()
    with psycopg2.connect(**db_config) as conn:
        cursor = conn.cursor()
        insert_query = """INSERT INTO vacancies 
        (vacancy_name, vacancy_url, company, area, education, salary, experience, employment , description, key_skills)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        insert_query2 = """UPDATE vacancies 
        SET vacancy_name=%s, company=%s, area=%s, education=%s, salary=%s, experience=%s, employment=%s, description=%s, key_skills=%s
        WHERE vacancy_url=%s
        """
        if type(datas[0]) != int:
            for data in datas:
                if not ((data.vacancy_url,) in urls):
                    cursor.execute(insert_query, (data.vacancy_name,
                                        data.vacancy_url,
                                        data.company,
                                        data.area,
                                        data.education,
                                        data.salary,
                                        data.experience,
                                        data.employment,
                                        data.description,
                                        data.key_skills))
                else:
                    cursor.execute(insert_query2,
                                   (data.vacancy_name,
                                        data.company,
                                        data.area,
                                        data.education,
                                        data.salary,
                                        data.experience,
                                        data.employment,
                                        data.description,
                                        data.key_skills, data.vacancy_url))

def get_urls():
    with psycopg2.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "SELECT vacancy_url FROM vacancies;"
        cursor.execute(query)
        answer = cursor.fetchall()
        return answer

def get_all_data(chat: int):
    with psycopg2.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM vacancies;"
        cursor.execute(query)
        #cursor.fetchmany(SIZE)
        answer = cursor.fetchall()
        datas = []
        if not answer == []:
            for i in answer:
                data = data_models.Data(chat_id=chat,
                                        vacancy_name=i[0],
                                        vacancy_url=i[1],
                                        company=i[2],
                                        area=i[3],
                                        education=i[4],
                                        salary=i[5],
                                        experience=i[6],
                                        employment=i[7],
                                        description=i[8],
                                        key_skills=i[9])
                datas.append(data)
        else:
            datas = [chat]
        save_data_to_file.save_to_file(datas)
