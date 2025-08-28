import json
import os

DATA_FILE = "students.json"

def load_data():
    """从 JSON 文件加载学生数据"""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """将学生数据保存到 JSON 文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_student():
    """添加新学生"""
    students = load_data()
    student_id = input("请输入学生学号: ")
    if student_id in students:
        print("错误: 该学号已存在。")
        return

    name = input("请输入学生姓名: ")
    age = input("请输入学生年龄: ")
    major = input("请输入学生专业: ")

    students[student_id] = {
        "name": name,
        "age": age,
        "major": major
    }
    save_data(students)
    print(f"成功添加学生: {name}")

def delete_student():
    """根据学号删除学生"""
    students = load_data()
    student_id = input("请输入要删除的学生的学号: ")
    if student_id not in students:
        print("错误: 未找到该学生。")
        return

    deleted_student_name = students[student_id]['name']
    del students[student_id]
    save_data(students)
    print(f"成功删除学生: {deleted_student_name}")

def update_student():
    """修改学生信息"""
    students = load_data()
    student_id = input("请输入要修改信息的学生的学号: ")
    if student_id not in students:
        print("错误: 未找到该学生。")
        return

    print("请输入新的信息 (如果不想修改某项，请直接按回车):")
    name = input(f"姓名 (当前: {students[student_id]['name']}): ")
    age = input(f"年龄 (当前: {students[student_id]['age']}): ")
    major = input(f"专业 (当前: {students[student_id]['major']}): ")

    if name:
        students[student_id]['name'] = name
    if age:
        students[student_id]['age'] = age
    if major:
        students[student_id]['major'] = major

    save_data(students)
    print("学生信息更新成功。")

def query_student():
    """查询单个学生信息"""
    students = load_data()
    student_id = input("请输入要查询的学生的学号: ")
    if student_id not in students:
        print("错误: 未找到该学生。")
        return

    student = students[student_id]
    print("\n--- 学生信息 ---")
    print(f"学号: {student_id}")
    print(f"姓名: {student['name']}")
    print(f"年龄: {student['age']}")
    print(f"专业: {student['major']}")
    print("------------------\n")


def display_all_students():
    """显示所有学生信息"""
    students = load_data()
    if not students:
        print("系统中没有学生信息。")
        return

    print("\n--- 所有学生信息 ---")
    for student_id, info in students.items():
        print(f"学号: {student_id}, 姓名: {info['name']}, 年龄: {info['age']}, 专业: {info['major']}")
    print("----------------------\n")

def main():
    """主菜单"""
    while True:
        print("\n欢迎使用学生信息管理系统")
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 修改学生信息")
        print("4. 查询学生信息")
        print("5. 显示所有学生")
        print("6. 退出")

        choice = input("请输入您的选择 (1-6): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            delete_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            query_student()
        elif choice == '5':
            display_all_students()
        elif choice == '6':
            print("感谢使用，再见！")
            break
        else:
            print("无效输入，请输入1到6之间的数字。")

if __name__ == "__main__":
    main()
