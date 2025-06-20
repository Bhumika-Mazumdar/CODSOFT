#### Task-01 ####

import sys
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QMessageBox, QListWidgetItem
)
from PyQt5.QtGui import QFont, QBrush, QColor
from database import init_db, add_task, get_tasks, update_task, delete_task, toggle_task

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
    QWidget {
        background-image: url("background.jpg");
        background-repeat: no-repeat;
        background-position: center;
    }
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }
    QPushButton {
        background-color: #91541f;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #a85d24;
    }
    QListWidget {
        background-color: rgba(255, 255, 255, 0.8);
        border: none;
    }
""")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.check_login)

        layout.addStretch()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(container)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "1234":
            self.todo = ToDoApp()
            self.todo.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()  # ✅ Ensure this is the FIRST line
        self.setWindowTitle("To-Do List App")
        self.setGeometry(100, 100, 400, 400)

        # Background styling
        self.setStyleSheet("""
    QWidget {
        background-image: url("background.jpg");
        background-repeat: no-repeat;
        background-position: center;
    }
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }
    QPushButton {
        background-color: #91541f;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #a85d24;
    }
    QListWidget {
        background-color: rgba(255, 255, 255, 0.8);
        border: none;
    }
""")

        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Input + Add button
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_task)

        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_btn)

        # Task List
        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.toggle_task)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        self.edit_btn.clicked.connect(self.edit_task)
        self.delete_btn.clicked.connect(self.delete_task)

        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)

        # Layout Setup
        layout.addLayout(input_layout)
        layout.addWidget(self.task_list)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_tasks(self):
        self.task_list.clear()
        tasks = get_tasks()
        for task in tasks:
            item = QListWidgetItem(task[1])
            item.setData(1000, task[0])  # store task ID
            if task[2]:
                item.setFont(QFont("", weight=QFont.Bold))
                item.setForeground(QBrush(QColor('green')))
                item.setText(f"✔ {task[1]}")
            self.task_list.addItem(item)

    def add_task(self):
        title = self.task_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Input Error", "Task cannot be empty.")
            return
        add_task(title)
        self.task_input.clear()
        self.load_tasks()

    def delete_task(self):
        selected = self.task_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "No task selected.")
            return
        task_id = selected.data(1000)
        delete_task(task_id)
        self.load_tasks()

    def edit_task(self):
        selected = self.task_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "No task selected.")
            return
        # At the top of the file, if not already imported

        # Inside edit_task:
        new_title, ok = QInputDialog.getText(self, "Edit Task", "New title:", text=selected.text().lstrip("✔ ").strip())

        if ok and new_title.strip():
            update_task(selected.data(1000), new_title.strip())
            self.load_tasks()

    def toggle_task(self, item):
        task_id = item.data(1000)
        completed = item.text().startswith("✔")
        toggle_task(task_id, 0 if completed else 1)
        self.load_tasks()

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
