import unittest
from unittest.mock import MagicMock
from app import app
import sqlite3


class TestCombinedWebsite(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def assert_status_code_200(self, response, message=""):
        self.assertEqual(response.status_code, 200,
                         f"Expected status code 200 but got {response.status_code}. {message}")

    # 用户故事 1：新生访问入学信息查询网站首页
    def test_user_story_1_case_1(self):
        response = self.client.get('/')
        self.assert_status_code_200(response, "Failed to access the home page.")

    def test_user_story_1_case_2(self):
        response = self.client.get('/')
        self.assert_status_code_200(response, "Failed to access the home page on second attempt.")

    # 用户故事 2：新生输入有效学号查询个人信息
    def test_user_story_2_case_1(self):
        # 模拟 StudentInfoStrategy 的 handle 方法
        mock_student_info_strategy = MagicMock()
        mock_student_info_strategy.handle.return_value = "name：Wenqi Dou，major：computer science"
        from app import StudentInfoStrategy
        app.StudentInfoStrategy = lambda: mock_student_info_strategy

        response = self.client.post('/', data=dict(question='jd123456'))
        self.assert_status_code_200(response, "Failed to get personal information with valid student ID.")
        expected = 'name：Wenqi Dou，major：computer science'
        self.assertIn(expected.encode('utf-8'), response.data,
                      "Incorrect personal information in the response.")

    def test_user_story_2_case_2(self):
        response = self.client.post('/', data=dict(question='jd123456'))
        self.assert_status_code_200(response, "Failed to get personal information with valid student ID.")

    def test_user_story_2_case_3(self):
        # 模拟数据库查询结果
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('Wenqi Dou', 'computer science')
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # 直接模拟 sqlite3.connect
        sqlite3.connect = MagicMock(return_value=mock_conn)

        response = self.client.post('/', data=dict(question='jd123456'))
        expected = 'name：Wenqi Dou，major：computer science'
        self.assertIn(expected.encode('utf-8'), response.data, "Incorrect personal information in the response.")

    # 用户故事 3：新生输入无效学号进行查询
    def test_user_story_3_case_2(self):
        response = self.client.post('/', data=dict(question='999999'))
        self.assert_status_code_200(response, "Failed to handle invalid student ID query.")

    def test_user_story_3_case_3(self):
        response = self.client.post('/', data=dict(question='999999'))
        self.assert_status_code_200(response, "Failed to handle invalid student ID query.")

    # 用户故事 4：新生查询入学需要带什么东西
    def test_user_story_4_case_1(self):
        response = self.client.post('/', data=dict(question='What do new students need to bring to school'))
        self.assert_status_code_200(response, "Failed to get school - bringing information.")

    def test_user_story_4_case_3(self):
        response = self.client.post('/', data=dict(question='What do new students need to bring to school'))
        self.assert_status_code_200(response, "Failed to get school - bringing information.")

    # 用户故事 5：新生在网站上反馈问题
    def test_user_story_5_case_1(self):
        # 模拟数据库插入操作
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # 直接模拟 sqlite3.connect
        sqlite3.connect = MagicMock(return_value=mock_conn)

        response = self.client.post('/feedback', data={'question': 'problem description', 'contact': '123456789'})
        self.assert_status_code_200(response, "Failed to submit feedback.")

    def test_user_story_5_case_2(self):
        # 模拟数据库插入操作
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # 直接模拟 sqlite3.connect
        sqlite3.connect = MagicMock(return_value=mock_conn)

        response = self.client.post('/feedback', data={'question': 'problem description', 'contact': '123456789'})
        self.assertIn(b'successful submission', response.data,
                      "Expected submission success message not in the response.")

    def test_user_story_5_case_3(self):
        # 模拟数据库插入操作
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # 直接模拟 sqlite3.connect
        sqlite3.connect = MagicMock(return_value=mock_conn)

        response = self.client.post('/feedback', data={'question': 'problem description', 'contact': '123456789'})
        mock_cursor.execute.assert_called_once_with("INSERT INTO feedbacks (question, contact) VALUES (?,?)",
                                                    ('problem description', '123456789'))
        mock_conn.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
