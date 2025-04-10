from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# 策略模式相关类定义
class QuestionHandlerStrategy:
    def handle(self, question):
        pass

class StudentInfoStrategy(QuestionHandlerStrategy):
    def handle(self, question):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT name, major FROM students WHERE student_id =?", (question,))
        result = c.fetchone()
        conn.close()
        if result:
            name, major = result
            return f'name：{name}，major：{major}'
        return None

class GeneralQAStrategy(QuestionHandlerStrategy):
    qa_dict = {
        "Where is the school located": "149 Sims Drive, Singapore 387380",
        "What do new students need to bring to school": "Passport, STP, enrolment contract, tuition payment record",
        "Where can I apply for STP": "10 Kallang Road #08 - 00 Singapore 208718 ICA Building"
    }
    def handle(self, question):
        return self.qa_dict.get(question)

# 初始化数据库
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (student_id TEXT PRIMARY KEY, name TEXT, major TEXT)''')
    c.execute("INSERT OR IGNORE INTO students VALUES ('jd123456', 'Wenqi Dou', 'computer science')")
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, contact TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # 首页只显示跳转按钮

@app.route('/qa', methods=['GET', 'POST'])
def qa_page():
    answer = None
    if request.method == 'POST':
        question = request.form.get('question')
        strategies = [StudentInfoStrategy(), GeneralQAStrategy()]
        for strategy in strategies:
            result = strategy.handle(question)
            if result:
                answer = result
                break
        if not answer:
            answer = "No information found"
    return render_template('qa.html', answer=answer)  # 问答页面模板

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    feedback_status = None
    if request.method == 'POST':
        question = request.form.get('question')
        contact = request.form.get('contact')
        if question and contact:
            conn = sqlite3.connect('students.db')
            c = conn.cursor()
            c.execute("INSERT INTO feedbacks (question, contact) VALUES (?,?)", (question, contact))
            conn.commit()
            conn.close()
            feedback_status ='successful submission'
        else:
            feedback_status ='submit failure'
    return render_template('feedback.html', feedback_status=feedback_status)  # 反馈页面模板

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

