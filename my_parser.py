import requests
import bs4
import data_models
from database import db_scripts
import save_data_to_file


def save_search(datas):
    save_data_to_file.save_to_file(datas)
    db_scripts.save_all_data(datas)


def main(main_data: data_models.Request):
    # так как приложение учебное, оно проходится только по 2 страницам,
    # но это не сложно исправить, если получить данные о количестве страниц
    # и просто проходиться вместо 2х по всем
    datas = []
    for page in range(2):
        # В параметре text - слово, которое вбиваем в поисковую строку
        # В параметре area - код региона(Москва 1, Санкт-Петербург 2, Подмосковье 2019)
        # В параметре education - образование(not_required_or_not_specified, higher, special_secondary)
        # В параметре salary указываем минимальную зарплату
        url = "https://hh.ru/search/vacancy?text={0}&area={1}&education={2}&salary={3}&only_with_salary=true&items_on_page=20&page={4}".format(
            main_data.text, main_data.area, main_data.education, main_data.salary, page)

        # Хэдхантер старается распознать искусственные запросы
        # передавая параметр headers мы не кажемся ему ботом и он возвращает код состояния 200, а не 403 или 404
        headers = {"Host": "hh.ru",
                   "User-Agent": "Safari",
                   "Accept": "*/*",
                   "Accept-Language": "ru",
                   "Connection": "keep-alive"}
        hh_request = requests.get(url, headers=headers)

        hh_soup = bs4.BeautifulSoup(hh_request.text, 'html.parser')
        paginator = hh_soup.find_all("span", {"class": "serp-item__title-link-wrapper"})

        for i in paginator:
            current_url = i.a['href']
            if "https://hh.ru/vacancy/" in current_url:
                current_hh_request = requests.get(current_url, headers=headers)
                current_hh_soup = bs4.BeautifulSoup(current_hh_request.text, 'html.parser')
                # Пытаемся выудить информацию со странички,
                # если не получается, пишем, что не нашли
                try:
                    current_area = current_hh_soup.find_all("span", {"data-qa": "vacancy-view-raw-address"})[0].text
                except Exception as err:
                    print(err)
                    if main_data.area == "1": current_area = "Москва"
                    if main_data.area == "2": current_area = "Санкт-Петербург"
                    if main_data.area == "2019": current_area = "Московская область"
                    if main_data.area == "": current_area = "Не указан"
                if main_data.education == "higher":
                    current_education = "Высшее образование"
                if main_data.education == "special_secondary":
                    current_education = "Среднее профессиональное образование"
                if main_data.education == "not_required_or_not_specified" or main_data.education == "":
                    current_education = "Не требуется"
                try:
                    current_salary = current_hh_soup.find_all("div", {"class": "vacancy-title"})[0].span.text
                    # current_salary_number = current_salary_text
                except Exception as err:
                    print(err)
                    current_salary = "Не найдено"
                try:
                    current_description = current_hh_soup.find_all("div", {"class": "g-user-content"},
                                  {"data-ka": "vacancy-description"})[0].text
                except Exception as err:
                    print(err)
                    current_description = "Не найдено"
                try:
                    current_experience = current_hh_soup.find_all("p", {"class": "vacancy-description-list-item"})[0].span.text
                except Exception as err:
                    print(err)
                    current_experience = "Не найдено"
                try:
                    current_employment = current_hh_soup.find_all("p", {"class": "vacancy-description-list-item"})[1].span.text
                except Exception as err:
                    print(err)
                    current_employment = "Не найдено"
                try:
                    current_name = current_hh_soup.find("div", {"class": "vacancy-title"}).h1.text
                except Exception as err:
                    print(err)
                    current_name = "Не найдено"
                try:
                    current_company = current_hh_soup.find_all("span", {
                        "class": "vacancy-company-name"})[0].a.span.text
                except Exception as err:
                    print(err)
                    current_company = "Не найдено"
                try:
                    key_skills = current_hh_soup.find_all("li", {"data-qa": "skills-element"})
                    for num_skill in range(len(key_skills)):
                        key_skills[num_skill] = key_skills[num_skill].div.div.text
                    key_skills = ", ".join(key_skills)
                    if key_skills == "":
                        key_skills = "Не указаны"
                except Exception as err:
                    print(err)
                    key_skills = "Не найдено"

                data = data_models.Data(chat_id=main_data.chat_id,
                                        vacancy_name=current_name,
                                        vacancy_url=current_url,
                                        company=current_company,
                                        area=current_area,
                                        education=current_education,
                                        salary=current_salary,
                                        experience=current_experience,
                                        employment=current_employment,
                                        description=current_description,
                                        key_skills=key_skills)
                datas.append(data)
                print(data)

        # Передаем id, чтобы функция сохранения знала, под каким именем сохранить
        # файл с фразой "Вакансии по вашему запросу не найдены"
        if datas == []:
            answer = [main_data.chat_id]
        else:
            answer = datas

        # Формируем файл по этому запросу и заносим данные в базу данных
        save_search(answer)

if __name__ == "__main__":
    data = data_models.Request(chat_id=1, text="программист", area="1", education="higher", salary="100000")
    main(data)
