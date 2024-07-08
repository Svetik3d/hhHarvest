from pydantic import BaseModel

# Все дагнные здесь применяются в конечном счете только для составления строк,
# поэтому все поля, кроме id чата, строки
class Request(BaseModel):
    chat_id: int
    text: str
    area: str = ""
    education: str = ""
    salary: str = ""


class Data(BaseModel):
    chat_id: int
    vacancy_name: str
    vacancy_url: str
    company: str
    area: str
    education: str
    salary: str
    experience: str
    employment: str
    description: str
    key_skills: str

