import json
import os

DATA_FILE = "students.json"

class StudentLogic:
    def __init__(self):
        self.students = self._load_data()

    def _load_data(self):
        """从 JSON 文件加载学生数据"""
        if not os.path.exists(DATA_FILE):
            return {}
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_data(self):
        """将学生数据保存到 JSON 文件"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.students, f, indent=4, ensure_ascii=False)

    def get_all_students(self):
        """获取所有学生信息的列表"""
        return self.students

    def query_student(self, student_id):
        """
        查询单个学生信息
        :param student_id: 学号
        :return: 学生信息字典，如果未找到则返回 None
        """
        return self.students.get(student_id)

    def add_student(self, student_id, name, age, major):
        """
        添加新学生
        :return: (bool, str) -> (操作是否成功, 消息)
        """
        if student_id in self.students:
            return False, "错误: 该学号已存在。"
        if not all([student_id, name, age, major]):
            return False, "错误: 所有字段都不能为空。"

        self.students[student_id] = {
            "name": name,
            "age": age,
            "major": major
        }
        self._save_data()
        return True, f"成功添加学生: {name}"

    def delete_student(self, student_id):
        """
        根据学号删除学生
        :return: (bool, str) -> (操作是否成功, 消息)
        """
        if student_id not in self.students:
            return False, "错误: 未找到该学生。"

        deleted_student_name = self.students[student_id]['name']
        del self.students[student_id]
        self._save_data()
        return True, f"成功删除学生: {deleted_student_name}"

    def update_student(self, student_id, name=None, age=None, major=None):
        """
        修改学生信息
        :return: (bool, str) -> (操作是否成功, 消息)
        """
        if student_id not in self.students:
            return False, "错误: 未找到该学生。"

        student = self.students[student_id]
        if name:
            student['name'] = name
        if age:
            student['age'] = age
        if major:
            student['major'] = major

        self._save_data()
        return True, "学生信息更新成功。"
