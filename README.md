from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 用于会话管理和闪现消息


# 数据库连接函数
def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn


# 初始化数据库
# 初始化数据库
# 数据库连接函数
def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    try:
        conn = get_db()  # 获取数据库连接
        c = conn.cursor()

        # 创建用户表
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        print("Users table created (or already exists).")

        # 创建任务表
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                priority TEXT,
                progress INTEGER,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        print("Tasks table created (or already exists).")

        conn.commit()  # 提交更改
        conn.close()   # 关闭数据库连接
    except Exception as e:
        print(f"Error initializing database: {e}")

# 用户登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash("登录成功", "success")
            return redirect(url_for('task_list'))
        else:
            flash("用户名或密码错误", "danger")

    return render_template('login.html')


# 用户登出路由
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("已登出", "info")
    return redirect(url_for('login'))


# 任务列表路由
@app.route('/')
def task_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE user_id = ?', (session['user_id'],))
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)


# 创建任务路由
@app.route('/task/create', methods=['GET', 'POST'])
def task_create():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        progress = request.form['progress']

        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO tasks (title, description, due_date, priority, progress, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, due_date, priority, progress, session['user_id']))
        conn.commit()
        conn.close()

        flash("任务创建成功！", "success")
        return redirect(url_for('task_list'))

    return render_template('task_form.html')


# 编辑任务路由
@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def task_edit(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE id = ? AND user_id = ?', (task_id, session['user_id']))
    task = c.fetchone()

    if not task:
        flash("任务不存在或权限不足", "danger")
        return redirect(url_for('task_list'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        progress = request.form['progress']

        c.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, priority = ?, progress = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, description, due_date, priority, progress, task_id))
        conn.commit()
        conn.close()

        flash("任务更新成功！", "success")
        return redirect(url_for('task_list'))

    conn.close()
    return render_template('task_edit.html', task=task)


# 删除任务路由
@app.route('/task/delete/<int:task_id>', methods=['GET'])
def task_delete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, session['user_id']))
    conn.commit()
    conn.close()

    flash("任务已删除！", "danger")
    return redirect(url_for('task_list'))


# 用户注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # 使用密码加密

        # 插入新用户
        conn = get_db()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('用户名已存在')
            return redirect(url_for('register'))

        return redirect(url_for('login'))  # 注册成功后重定向到登录页面

    return render_template('register.html')



if __name__ == '__main__':
    init_db()  # 初始化数据库
    app.run(debug=True, use_reloader=False)  # 禁用自动重载，避免多进程问题
