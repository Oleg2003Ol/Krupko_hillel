from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        #Проверка есть ли логин в списке
        with open("test.txt", "r") as file:
            users = file.readlines()
            for user in users:
                if name in user:
                    return redirect(url_for('login'))
        #Внос логина и пароля в список
        with open("test.txt", "a") as file:
            file.write(f"{name} {password}\n")
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        with open("test.txt", "r") as file:
            users = file.readlines()
            for user in users:
                if name in user:
                    lst_password = user.split()[1]
                    if password == lst_password:
                        return "Вы в системе"
                    else:
                        return "Не правильный логин или пароль"
            else:
                return "Вы не зарегистрированны" #добавил от себя графу проверки на регистрацию в вьюшке login

    return render_template("index.html")
