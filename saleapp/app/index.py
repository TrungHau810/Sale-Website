import math
from flask import render_template, request, redirect, session, jsonify
import dao, utils
from app import app, login
from flask_login import login_user, logout_user
from app.models import UserRole


@app.route('/')
def index():
    page = request.args.get("page", 1)
    kw = request.args.get('kw')
    prods = dao.load_products(kw=kw, page=int(page))

    page_size = app.config["PAGE_SIZE"]
    total = dao.count_products()
    return render_template("index.html", products=prods, pages=math.ceil(total / page_size))


@app.route('/register', methods=['get', 'post'])
def register_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if not password.__eq__(confirm):
            err_msg = 'Mật khẩu không khớp'
        else:
            data = request.form.copy()
            del data['confirm']
            avatar = request.files.get('avatar')
            dao.add_user(avatar=avatar, **data)
            return redirect("/login")

    return render_template('register.html', err_msg=err_msg)


@app.route("/login", methods=['get', 'post'])
def login_view():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect("/")
    return render_template('login.html')


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    # # Ví dụ về cấu trúc giỏ hàng -> Tạo dạng dictionary
    # {
    #     # Add 1 sản phẩm mới
    #     '1':{
    #         'id': 1,
    #         'name': 'ABC',
    #         'price': 10,
    #         # Số lượng món hàng. Mặc định là 1
    #         # Nếu add thêm sản phẩm giống nhau -> Tăng 'quantity'
    #         'quantity': 1
    #     }
    #     #Add thêm sản phẩm mới
    #     '2':{
    #         'id': 2,
    #         'name': 'iphone',
    #         'price': 15,
    #         'quantity': 1
    #     }
    # }
    cart = session.get('cart')
    if not cart:
        cart = {}

    # Lấy id, name, price
    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')

    # Kiểm tra sản phẩm có trong cart
    if id in cart:
        # Tăng số lượng
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart
    return jsonify(utils.cart_stats(cart))

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/login-admin", methods=['post'])
def login_admin_view():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect("/admin")

@app.route("/cart")
def cart_view():
    return render_template("cart.html")

@app.context_processor
def common_response_data():
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.cart_stats(session.get('cart'))
    }

if __name__ == '__main__':
    with app.app_context():
        from app import admin

        app.run(debug=True)
