from functools import wraps
from flask import render_template, request, redirect, flash
from .app import app, db, login_manager
from .models import Item, Categories, Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .user_login import UserLogin
import base64

# фабрика класса UserLogin для обработки авторизации
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)

# фильтр b64encode, который кодирует бинарные данные в base64-строку
@app.template_filter('b64encode')
def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

# декоратор для проверки на админа
def admin_required(func):
    @wraps(func)
    @login_required
    def decorated_view(*args, **kwargs):
        if current_user.is_admin():
            return func(*args, **kwargs)
        else:
            return render_template('admin_nead_roots_rights.html')
    return decorated_view

########################
# ПОЛЬЗОВАТЕЛЬСКИЕ ВЬЮХИ
# стартовая страница
@app.route('/')
def index():
    return render_template('index.html')

# авторизация пользователей
@app.route('/login', methods=['POST', 'GET'])
def login():
    # если авторизация пройдена, перебросит в стартовую
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        # если пользователь найден и хешт паролей совпали
        if user and check_password_hash(user.password, password):
            # создаём объект обработки учётных данных
            userlogin = UserLogin().create(user)

            # считываем выбор галки "Запомнить"
            try:
                # если галка не выбрана шарахнет исключение
                val = request.form['remain']
                rm = True
            except:
                rm = False

            # стартуем сессию пользователя
            login_user(userlogin, remember=rm)

            # если пользак пытался пробиться на страницу (где нужна авторизация),
            # то сразу после авторизации, пользака на ней и перекинет
            return redirect(request.args.get("next") or '/')
        else:
            flash('Неправильный email или пароль')
            return render_template('login.html')
    else:
        return render_template('login.html')

# выход из учётки
@app.route('/logout')
@login_required
def logout():
    # закрываем сессию пользака
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect('/login')

# форма регистрации пользователей
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        user = Users.query.filter_by(email=email).all()
        if not name or not email:
            flash('Поля не могу быть пустыми')
        else:
            if user:
                flash('Пользователь с таким email уже зарегистрирован')
            else:
                password = request.form['password']
                password_again = request.form['password_again']
                if password != password_again:
                    flash('Пароли не совпадают')
                else:
                    hash = generate_password_hash(password)

                    user = Users(name=name,
                                 email=email,
                                 password=hash)

                    try:
                        db.session.add(user)
                        db.session.commit()
                        return redirect('/')
                    except:
                        flash('При регистрации произошла ошибка')

    return render_template('registration.html')

# просмотр списка товаров
@app.route('/item', methods=['POST', 'GET'])
@app.route('/item/<int:page>', methods=['POST', 'GET'])
def item(page=1):
    if request.method == 'POST':
        search_query = request.form['search']
        # вывод через пагинацию по 4 элемента, начиная с первой выборки элементов
        items = Item.query.filter(Item.name.contains(search_query)).paginate(page=page, per_page=4, error_out=False)
        return render_template('item.html', items=items)
    else:
        # вывод через пагинацию по 4 элемента, начиная с первой выборки элементов
        items = Item.query.paginate(page=page, per_page=4, error_out=False)
        # вывод общего количества страниц
        # print(items.pages)
        # вывод номера предыдущей страницы (либо None)
        # print(items.prev_num)
        # вывод номера следующей страницы (либо None)
        # print(items.next_num)
        return render_template('item.html', items=items)

# просмотр товара
@app.route('/item/view/<int:id>', methods=['POST', 'GET'])
def item_view(id):
    item = Item.query.get_or_404(id)
    return render_template('item_view.html', item=item)

#################
# АДМИНСКИЕ ВЬЮХИ
# просмотр списка товаров
@app.route('/admin/item', methods=['POST', 'GET'])
@admin_required
def admin_item():
    if request.method == 'POST':
        search_query = request.form['search']
        items = Item.query.filter(Item.name.contains(search_query)).all()
        return render_template('admin_item.html', items=items)
    else:
        items = Item.query.all()
        return render_template('admin_item.html', items=items)

# добавление товара
@app.route('/admin/item/add', methods=['POST', 'GET'])
@admin_required
def admin_item_add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        image1 = request.files['image1'].read() or None
        image2 = request.files['image2'].read() or None
        image3 = request.files['image3'].read() or None
        image4 = request.files['image4'].read() or None
        price = request.form['price']

        item = Item(name=name,
                    category=category,
                    description=description,
                    price=price,
                    image1=image1,
                    image2=image2,
                    image3=image3,
                    image4=image4)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/admin/item')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        categories = Categories.query.all()
        return render_template('admin_item_add.html', categories=categories)

# просмотр и редактирование товара
@app.route('/admin/item/view/<int:id>', methods=['POST', 'GET'])
@admin_required
def admin_item_view(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.category = request.form['category']
        item.description = request.form['description']
        item.price = request.form['price']
        item.image1 = request.files['image1'].read() or item.image1
        item.image2 = request.files['image2'].read() or item.image2
        item.image3 = request.files['image3'].read() or item.image3
        item.image4 = request.files['image4'].read() or item.image4
        try:
            db.session.commit()
            return redirect('/admin/item')
        except:
            return "При обновлении статьи произошла ошибка"
    else:
        categories = Categories.query.all()
        return render_template('admin_item_view.html', item=item, categories=categories)

# удаление товара
@app.route('/admin/item/del/<int:id>')
@admin_required
def admin_item_delete(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/admin/item')
    except:
        return "При удалении статьи произошла ошибка"