static/styles.css

body {
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    flex-direction: column;
    background-color: #f0f0f0;
}

.container {
    text-align: center;
}

button {
    padding: 10px 20px;
    font-size: 16px;
    margin: 10px;
    cursor: pointer; /* Добавляем курсор для кнопок */
}

input[type="text"] {
    padding: 10px;
    font-size: 16px;
    margin: 10px;
}

.buttons-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.button {
    margin: 5px;
    padding: 10px;
    border-radius: 5px;
    /* cursor: pointer; */
    width: auto;
    min-width: 120px;
    text-align: center;
}

.small-button {
    padding: 0px 2px;  /* Уменьшите отступы, чтобы сделать кнопку меньше */
    font-size: 16px;    /* Уменьшите размер шрифта */
    /* border: none;       /* Уберите рамку, если она не нужна */
    /* border-radius: 3px; /* Добавьте скругление углов */
    cursor: pointer;    /* Измените курсор на указатель */
}


templates/edit_button.html

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Изменить кнопку</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
<div class="container">
    <h1>Изменить кнопку</h1>
    <form method="POST">
        <input type="text" name="when" placeholder="Когда?" maxlength="152" value="{{ button.when }}" required>
        <input type="text" name="where" placeholder="Где?" maxlength="152" value="{{ button.where }}">
        <input type="text" name="who" placeholder="Кто?" maxlength="152" value="{{ button.who }}">
        <button type="submit">Сохранить</button>
    </form>
    <button onclick="window.location.href='{{ url_for('edit_schedule', schedule_id=button.schedule_id) }}'">Назад к расписанию</button>
</div>
</body>
</html>


templates/home.html

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Пароль расписания</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <script>
        // Функция для скрытия сообщения через 3 секунды
        function hideMessage() {
            const message = document.getElementById('error-message');
            if (message) {
                setTimeout(() => {
                    message.style.display = 'none';
                }, 3000);
            }
        }

        // Запуск функции при загрузке страницы
        window.onload = hideMessage;
    </script>
</head>
<body>
<div class="container">
    <h1>Индивидуальное расписание</h1>
    <h3>Чтобы создать новое расписание, придумайте любой пароль. Главное - его запомнить.</h3>

    <!-- Форма для создания расписания -->
    <form action="/create_schedule" method="POST">
        <input type="text" name="new_password" placeholder="Новый пароль" required maxlength="152">
        <button type="submit">Создать расписание</button>
    </form>


    {% if error %}
    <div id="error-message" style="color: red;">{{ error }}</div>
    {% endif %}


    <!-- Форма для просмотра расписания -->
    <form action="/view_schedule" method="POST">
        <input type="text" name="password" placeholder="Сохранённый пароль" required maxlength="152">
        <button type="submit">Открыть расписание</button>
    </form>
</div>
</body>
</html>


templates/schedule.html

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Расписание</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
<div class="container">
    <h1>Создать событие</h1>
    <form method="POST">
        <input type="text" name="when" placeholder="Когда?" required maxlength="152">
        <input type="text" name="where" placeholder="Где?" maxlength="152">
        <input type="text" name="who" placeholder="Кто?" maxlength="152">
        <button type="submit">Сохранить</button>
    </form>
    <h2>События</h2>  <!-- Исправлено здесь -->
    <div class="buttons-container">
        {% for button in buttons %}
        <div class="button" style="background-color: {{ button.color }};">
            {{ button.when }} {{ button.where }} {{ button.who }}
            <span>{{ button.name }}</span>
            <!-- Обернуть кнопки в отдельный контейнер -->
            <div class="button-controls">
                <button class="small-button"
                        onclick="window.location.href='{{ url_for('edit_button', button_id=button.id) }}'">Изменить
                </button>
                <form action="{{ url_for('delete_button', button_id=button.id) }}" method="POST"
                      style="display:inline;">
                    <button class="small-button" type="submit"
                            onclick="return confirm('Вы уверены, что хотите удалить эту кнопку?');">Удалить
                    </button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>

    <form action="{{ url_for('delete_schedule', schedule_id=schedule.id) }}" method="POST" style="display:inline;">
        <button type="submit" onclick="return confirm('Вы уверены, что хотите удалить это расписание?');">Удалить
            расписание
        </button>
    </form>
    <button onclick="window.location.href='{{ url_for('home') }}'">Назад на главную</button>
</div>
</body>
</html>


/app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Замените 'name' на '__name__'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), unique=True, nullable=False)
    buttons = db.relationship('Button', backref='schedule', lazy=True)


class Button(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    when = db.Column(db.String(100), nullable=True)
    where = db.Column(db.String(100), nullable=True)
    who = db.Column(db.String(100), nullable=True)
    color = db.Column(db.String(20), nullable=False)


# Создание базы данных, если она еще не существует
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    error = request.args.get('error')
    return render_template('home.html', error=error)


@app.route('/create_schedule', methods=['POST'])
def create_schedule():
    new_password = request.form['new_password']

    # Проверка, существует ли уже расписание с таким паролем
    existing_schedule = Schedule.query.filter_by(password=new_password).first()
    if existing_schedule:
        # Если пароль уже существует, перенаправим на главную страницу с ошибкой или сообщением
        return redirect(url_for('home', error="Этот пароль уже используется."))

    new_schedule = Schedule(password=new_password)
    db.session.add(new_schedule)
    db.session.commit()
    return redirect(url_for('edit_schedule', schedule_id=new_schedule.id))


@app.route('/view_schedule', methods=['POST'])
def view_schedule():
    password = request.form['password']
    schedule = Schedule.query.filter_by(password=password).first()
    if not schedule:
        # Если расписание не найдено, перенаправляем на главную страницу с ошибкой
        return redirect(url_for('home', error="Этот пароль еще не используется."))

    return redirect(url_for('edit_schedule', schedule_id=schedule.id))


@app.route('/edit_schedule/<int:schedule_id>', methods=['GET', 'POST'])
def edit_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if request.method == 'POST':
        when = request.form.get('when')
        where = request.form.get('where')
        who = request.form.get('who')
        color = 'lightgreen' if not who else 'pink'

        if color and (when or where):
            new_button = Button(schedule_id=schedule.id, when=when, where=where, who=who, color=color)
            db.session.add(new_button)
            db.session.commit()
            return redirect(url_for('edit_schedule', schedule_id=schedule.id))

        return redirect(url_for('edit_schedule', schedule_id=schedule.id))

    buttons = Button.query.filter_by(schedule_id=schedule.id).all()
    return render_template('schedule.html', schedule=schedule, buttons=buttons)


@app.route('/edit_button/<int:button_id>', methods=['GET', 'POST'])
def edit_button(button_id):
    button = Button.query.get(button_id)

    if request.method == 'POST':
        when = request.form.get('when')
        where = request.form.get('where')
        who = request.form.get('who')

        # Проверка, заполнено ли поле "Когда?"
        if not when:
            return redirect(url_for('edit_schedule', schedule_id=button.schedule_id))

        # Изменение цвета кнопки на светло-изумрудный, если "Кто?" не заполнено
        color = 'lightgreen' if not who else 'pink'

        # Обновление информации о кнопке
        button.when = when
        button.where = where
        button.who = who
        button.color = color

        db.session.commit()
        return redirect(url_for('edit_schedule', schedule_id=button.schedule_id))

    return render_template('edit_button.html', button=button)


@app.route('/save_password/<int:schedule_id>', methods=['POST'])
def save_password(schedule_id):
    password = request.form['password']
    schedule = Schedule.query.get(schedule_id)
    schedule.password = password
    db.session.commit()
    return redirect(url_for('edit_schedule', schedule_id=schedule.id))


@app.route('/delete_button/<int:button_id>', methods=['POST'])
def delete_button(button_id):
    button = Button.query.get(button_id)
    if button:
        schedule_id = button.schedule_id  # Сохраняем идентификатор расписания
    db.session.delete(button)
    db.session.commit()
    return redirect(url_for('edit_schedule', schedule_id=schedule_id))  # Перенаправляем на редактирование расписания


@app.route('/delete_schedule/<int:schedule_id>', methods=['POST'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if schedule:
        # Получаем все кнопки, связанные с этим расписанием
        buttons = Button.query.filter_by(schedule_id=schedule_id).all()
        # Удаляем все кнопки
        for button in buttons:
            db.session.delete(button)
        # Удаляем само расписание
        db.session.delete(schedule)
        db.session.commit()
    return redirect(url_for('home'))  # Замените 'home' на ваше имя маршрута для главной страницы


if __name__ == '__main__':  # Замените 'name' на '__name__'
    app.run(debug=True)

