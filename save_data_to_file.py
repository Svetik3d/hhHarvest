import data_models
import texts

def form_to_str(data: data_models.Data):
    answer = texts.forma.format(data.vacancy_name, data.vacancy_url,
                                data.company, data.area, data.education,
                                data.salary, data.experience, data.employment,
                                data.description, data.key_skills)
    return answer


def save_to_file(datas):
    result_str = ""
    if type(datas[0]) == int:
        result_str = "Вакансии по вашему запросу не найдены."
        chat_id = datas[0]
    else:
        for i in range(len(datas)):
            result_str += "{0}.".format(i+1)+form_to_str(datas[i])+"\n"
        chat_id = datas[0].chat_id
    with open("{0}.txt".format(chat_id), mode='w+', encoding='utf-8') as f:
        f.write(result_str)