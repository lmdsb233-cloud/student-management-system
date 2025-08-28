from student_logic import StudentLogic

def add_student(logic):
    """处理添加新学生的命令行交互"""
    student_id = input("请输入学生学号: ")
    name = input("请输入学生姓名: ")
    age = input("请输入学生年龄: ")
    major = input("请输入学生专业: ")
    success, message = logic.add_student(student_id, name, age, major)
    print(message)

def delete_student(logic):
    """处理删除学生的命令行交互"""
    student_id = input("请输入要删除的学生的学号: ")
    success, message = logic.delete_student(student_id)
    print(message)

def update_student(logic):
    """处理修改学生信息的命令行交互"""
    student_id = input("请输入要修改信息的学生的学号: ")
    student = logic.query_student(student_id)
    if not student:
        print("错误: 未找到该学生。")
        return

    print("请输入新的信息 (如果不想修改某项，请直接按回车):")
    name = input(f"姓名 (当前: {student['name']}): ")
    age = input(f"年龄 (当前: {student['age']}): ")
    major = input(f"专业 (当前: {student['major']}): ")

    # Create a dictionary with only the provided values
    update_data = {}
    if name:
        update_data['name'] = name
    if age:
        update_data['age'] = age
    if major:
        update_data['major'] = major

    if not update_data:
        print("没有输入任何新的信息，操作取消。")
        return

    success, message = logic.update_student(student_id, **update_data)
    print(message)

def query_student(logic):
    """处理查询单个学生信息的命令行交互"""
    student_id = input("请输入要查询的学生的学号: ")
    student = logic.query_student(student_id)
    if not student:
        print("错误: 未找到该学生。")
        return

    print("\n--- 学生信息 ---")
    print(f"学号: {student_id}")
    print(f"姓名: {student['name']}")
    print(f"年龄: {student['age']}")
    print(f"专业: {student['major']}")
    print("------------------\n")

def display_all_students(logic):
    """处理显示所有学生信息的命令行交互"""
    students = logic.get_all_students()
    if not students:
        print("系统中没有学生信息。")
        return

    print("\n--- 所有学生信息 ---")
    for student_id, info in students.items():
        print(f"学号: {student_id}, 姓名: {info['name']}, 年龄: {info['age']}, 专业: {info['major']}")
    print("----------------------\n")

def main():
    """主菜单"""
    logic = StudentLogic()

    while True:
        print("\n欢迎使用学生信息管理系统 (命令行版)")
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 修改学生信息")
        print("4. 查询学生信息")
        print("5. 显示所有学生")
        print("6. 退出")

        choice = input("请输入您的选择 (1-6): ")

        if choice == '1':
            add_student(logic)
        elif choice == '2':
            delete_student(logic)
        elif choice == '3':
            update_student(logic)
        elif choice == '4':
            query_student(logic)
        elif choice == '5':
            display_all_students(logic)
        elif choice == '6':
            print("感谢使用，再见！")
            break
        else:
            print("无效输入，请输入1到6之间的数字。")

if __name__ == "__main__":
    main()
