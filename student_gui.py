import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QMessageBox, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

from student_logic import StudentLogic

class StudentGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = StudentLogic()
        self.init_ui()
        self.connect_signals()
        self.load_students_to_list()

    def init_ui(self):
        self.setWindowTitle('学生信息管理系统 by Jules')
        self.setGeometry(100, 100, 800, 600)
        self.setup_styles()

        # Main layout
        main_layout = QHBoxLayout(self)

        # Left side: Student list
        left_layout = QVBoxLayout()
        self.student_list_widget = QListWidget()
        left_layout.addWidget(QLabel('所有学生:'))
        left_layout.addWidget(self.student_list_widget)

        # Right side: Form and buttons
        right_layout = QVBoxLayout()

        # Form
        form_layout = QVBoxLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('学号')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('姓名')
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText('年龄')
        self.major_input = QLineEdit()
        self.major_input.setPlaceholderText('专业')

        form_layout.addWidget(QLabel('学生信息:'))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.age_input)
        form_layout.addWidget(self.major_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton('添加')
        self.update_btn = QPushButton('修改')
        self.delete_btn = QPushButton('删除')
        self.clear_btn = QPushButton('清空表单')

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.clear_btn)

        right_layout.addLayout(form_layout)
        right_layout.addLayout(button_layout)
        right_layout.addStretch() # Pushes everything up

        main_layout.addLayout(left_layout, 2)  # 2/3 of the space
        main_layout.addLayout(right_layout, 1) # 1/3 of the space

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #a8d8ff;
                color: black;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
        """)

    def connect_signals(self):
        """Connect all signals to slots."""
        self.student_list_widget.itemClicked.connect(self.on_student_selected)
        self.add_btn.clicked.connect(self.add_student)
        self.update_btn.clicked.connect(self.update_student)
        self.delete_btn.clicked.connect(self.delete_student)
        self.clear_btn.clicked.connect(self.clear_form)

    def load_students_to_list(self):
        """Loads all students from logic and populates the QListWidget."""
        self.student_list_widget.clear()
        students = self.logic.get_all_students()
        for student_id, info in students.items():
            item_text = f"{student_id}: {info['name']} ({info['major']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, student_id) # Store ID in the item
            self.student_list_widget.addItem(item)

    def on_student_selected(self, item):
        """Fills the form when a student is selected from the list."""
        student_id = item.data(Qt.ItemDataRole.UserRole)
        student_info = self.logic.query_student(student_id)
        if student_info:
            self.id_input.setText(student_id)
            self.id_input.setReadOnly(True) # Prevent editing ID of existing student
            self.name_input.setText(student_info['name'])
            self.age_input.setText(student_info['age'])
            self.major_input.setText(student_info['major'])

    def add_student(self):
        """Handles the 'Add' button click."""
        student_id = self.id_input.text()
        name = self.name_input.text()
        age = self.age_input.text()
        major = self.major_input.text()

        success, message = self.logic.add_student(student_id, name, age, major)
        self.show_message("添加学生", message)
        if success:
            self.load_students_to_list()
            self.clear_form()

    def update_student(self):
        """Handles the 'Update' button click."""
        student_id = self.id_input.text()
        if not student_id:
            self.show_message("错误", "请先从列表中选择一个学生。")
            return

        name = self.name_input.text()
        age = self.age_input.text()
        major = self.major_input.text()

        success, message = self.logic.update_student(student_id, name, age, major)
        self.show_message("修改信息", message)
        if success:
            self.load_students_to_list()
            self.clear_form()

    def delete_student(self):
        """Handles the 'Delete' button click."""
        student_id = self.id_input.text()
        if not student_id:
            self.show_message("错误", "请先从列表中选择一个学生。")
            return

        # Confirmation dialog
        reply = QMessageBox.question(self, '删除确认',
                                     f"您确定要删除学号为 {student_id} 的学生吗?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.logic.delete_student(student_id)
            self.show_message("删除学生", message)
            if success:
                self.load_students_to_list()
                self.clear_form()

    def clear_form(self):
        """Clears all input fields and resets ID field."""
        self.id_input.clear()
        self.id_input.setReadOnly(False)
        self.name_input.clear()
        self.age_input.clear()
        self.major_input.clear()
        self.student_list_widget.clearSelection()

    def show_message(self, title, message):
        """Helper to show a message box."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentGUI()
    window.show()
    sys.exit(app.exec())
