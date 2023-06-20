from flask import render_template, request, redirect
from .app import app, db
from .models import Item, Categories
import base64

# ПОЛЬЗОВАТЕЛЬСКИЕ ВЬЮХИ
# стартовая страница
@app.route('/')
def index():
    return render_template('index.html')

# АДМИНСКИЕ ВЬЮХИ
# просмотр списка товаров
@app.route('/admin/item', methods=['POST', 'GET'])
def admin_item():
    if request.method == 'POST':
        search_query = request.form['search']
        items = Item.query.filter(Item.name.contains(search_query)).all()
        return render_template('admin_item.html', items=items)
    else:
        items = Item.query.all()
        return render_template('admin_item.html', items=items)

# фильтр b64encode, который кодирует бинарные данные в base64-строку
@app.template_filter('b64encode')
def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

# добавление товара
@app.route('/admin/item/add', methods=['POST', 'GET'])
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
def admin_item_delete(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/admin/item')
    except:
        return "При удалении статьи произошла ошибка"