from fastapi import FastAPI
import uvicorn

app = FastAPI()

my_books = {
    "novelty": [
        {"id": 1, "image": "/finals.jpg", "title": "Исход(ы)", "author": "Джулиан Барнс", "oldPrice": 890, "price": 712},
        {"id": 2, "image": "/ninth.jpg", "title": "Девятый", "author": "Сергей Лукьяненко", "oldPrice": 750, "price": 600},
        {"id": 3, "image": "/mercury.jpg", "title": "Ртуть", "author": "Калли Харт", "oldPrice": 890, "price": 712},
        {"id": 4, "image": "/mask.jpg", "title": "Космос ближе: Как Илон Маск и инженеры SpaceX поставили полеты на поток", "author": "Эрик Бергер", "oldPrice": 1200, "price": 960},
        {"id": 5, "image": "/knight.jpg", "title": "Чёрный рыцарь", "author": "Рина Кент", "oldPrice": 650, "price": 520}
    ],
    "anime": [
        {"id": 6, "image": "/name.jpg", "title": "Твоё имя", "author": "Макото Синкай", "oldPrice": 1200, "price": 990},
        {"id": 7, "image": "/voice.jpg", "title": "Форма голоса", "author": "Ёситоки Ойма", "oldPrice": 1100, "price": 880},
        {"id": 8, "image": "/ghosts.jpg", "title": "Унесённые призраками", "author": "Хаяо Миядзаки", "oldPrice": 1350, "price": 1090},
        {"id": 9, "image": "/castle.jpg", "title": "Ходячий замок", "author": "Диана Уинн Джонс", "oldPrice": 1250, "price": 999},
        {"id": 10, "image": "/grave.jpg", "title": "Могила светлячков", "author": "Акиюки Носака", "oldPrice": 950, "price": 760}
    ],
    "study": [
        {"id": 11, "image": "/vas.jpg", "title": "JavaScript для начинающих", "author": "Алексей Васильев", "oldPrice": 1200, "price": 990},
        {"id": 12, "image": "/lutz.jpg", "title": "Python с нуля", "author": "Марк Лутц", "oldPrice": 1500, "price": 1290},
        {"id": 13, "image": "/react.jpg", "title": "React в действии", "author": "Алекс Бэнкс", "oldPrice": 1800, "price": 1490},
        {"id": 14, "image": "/inter.jpg", "title": "Дизайн интерфейсов", "author": "Алан Купер", "oldPrice": 2100, "price": 1790},
        {"id": 15, "image": "/cc.jpg", "title": "Алгоритмы и структуры данных", "author": "Роберт Седжвик", "oldPrice": 2500, "price": 1990}
    ]
}


@app.get ("/books/{category}")
def get_books_by_category(category:str):
    books = my_books.get(category,[])
    return {"books":books}


@app.post("/category/add")
def add_category(cat_name:str):
    if cat_name not in my_books:
        my_books[cat_name] = []
        return {f" Категория {cat_name} создана"}
    return {"Данная категория уже существует"}



if __name__ == '__main__':
    uvicorn.run(app,host= "0.0.0.0", port=8000)





