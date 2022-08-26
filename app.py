import sys
import sqlite3
import pyperclip
from PyQt5.Qt import *


class Passwords(QWidget):
    def __init__(self, parent=None):
        super(Passwords, self).__init__(parent)

        self.passwords = self.get_passwords()
        font = QFont('Calibri', 14)

        main_layout = QVBoxLayout()
        search_input_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        add_password_layout = QHBoxLayout()
        name_layout = QVBoxLayout()
        password_layout = QVBoxLayout()
        add_password_button_layout = QVBoxLayout()

        self.searchInputDefinition = QLabel("Поиск")
        self.searchInputDefinition.setFont(QFont('Calibri', 12))
        self.searchInput = QLineEdit("")
        self.searchInput.setReadOnly(False)
        self.searchInput.returnPressed.connect(self.copy_password)

        self.searchDropDown = QComboBox()
        self.searchDropDown.addItems(self.passwords.keys())
        self.searchDropDown.currentIndexChanged.connect(self.drop_down_change)

        self.searchButton = QPushButton("Скопировать")
        self.searchButton.clicked.connect(self.copy_password)

        self.searchSuccess = QLabel("")

        self.searchInput.setFont(font)
        self.searchDropDown.setFont(font)
        self.searchButton.setFont(font)
        self.searchSuccess.setFont(QFont('Calibri', 12))

        self.addNameInputDefinition = QLabel("Сервис")
        self.addNameInputDefinition.setFont(QFont('Calibri', 12))
        self.addNameInput = QLineEdit("")
        self.addNameInput.setFont(font)
        self.addNameInput.setReadOnly(False)

        self.addPasswordInputDefinition = QLabel("Пароль")
        self.addPasswordInputDefinition.setFont(QFont('Calibri', 12))
        self.addPasswordInput = QLineEdit("")
        self.addPasswordInput.setReadOnly(False)
        self.addPasswordInput.setFont(font)

        self.addPasswordEmptyLabel = QLabel("")
        self.addPasswordButton = QPushButton("Создать")
        self.addPasswordButton.clicked.connect(self.create_password)
        self.addPasswordButton.setFont(font)

        self.addSuccess = QLabel("")
        self.addSuccess.setFont(QFont('Calibri', 12))

        add_password_button_layout.addWidget(self.addPasswordEmptyLabel)
        add_password_button_layout.addWidget(self.addPasswordButton)

        name_layout.addWidget(self.addNameInputDefinition)
        name_layout.addWidget(self.addNameInput)

        password_layout.addWidget(self.addPasswordInputDefinition)
        password_layout.addWidget(self.addPasswordInput)

        add_password_layout.addLayout(name_layout)
        add_password_layout.addLayout(password_layout)
        add_password_layout.addLayout(add_password_button_layout)

        search_input_layout.addWidget(self.searchInputDefinition)

        search_layout.addWidget(self.searchInput)
        search_layout.addWidget(self.searchDropDown)
        search_layout.addWidget(self.searchButton)

        main_layout.addLayout(search_input_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.searchSuccess)
        main_layout.addLayout(add_password_layout)
        main_layout.addWidget(self.addSuccess)
        self.setLayout(main_layout)

        self.setWindowTitle("Vault-Warden")

    def drop_down_change(self):
        for f in self.passwords:
            if f == self.searchDropDown.currentText():
                self.copy_text(self.passwords[f])
                pass

    @pyqtSlot()
    def copy_password(self):
        for password in self.passwords:
            if self.searchInput.text().lower() in password.lower():
                self.copy_text(self.passwords[password])
                pass

    def create_password(self):
        new_service = self.addNameInput.text()
        new_password = self.addPasswordInput.text()
        con = sqlite3.Connection("app.db")
        cur = con.cursor()
        cur.execute("""INSERT INTO passwords(name, password) VALUES("{name}", "{password}")""".format(name=new_service,
                                                                                                      password=new_password))
        con.commit()
        cur.close()
        con.close()
        self.addNameInput.setText("")
        self.addPasswordInput.setText("")
        self.addSuccess.setText("Сохранено!")
        self.addSuccess.setStyleSheet("background-color: #00FF00;")

    def copy_text(self, text):
        pyperclip.copy(text)
        self.searchSuccess.setText("Скопировано!")
        self.searchSuccess.setStyleSheet("background-color: #00FF00;")

    def get_passwords(self):
        con = sqlite3.Connection("app.db")
        cur = con.cursor()
        cur.execute("SELECT name, password FROM passwords")
        passwords = cur.fetchall()
        words = dict()
        for password in passwords:
            words[password[0]] = password[1]
        cur.close()
        con.close()
        return words


def main():
    app = QApplication(sys.argv)
    ex = Passwords()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
