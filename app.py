import sys
import subprocess
import sqlite3

from PyQt5.Qt import *

DATABASE_NAME = "app.db"


class PasswordStorage:

    @staticmethod
    def db_connect(func):
        def wrapper(*args, **kwargs):
            connection = sqlite3.Connection(DATABASE_NAME)
            cursor = connection.cursor()
            result = func(cursor, connection, *args, **kwargs)
            cursor.close()
            connection.close()
            return result
        return wrapper

    @staticmethod
    @db_connect
    def fetch_passwords(cursor, *args, **kwargs) -> dict:
        cursor.execute("SELECT name, password FROM passwords")
        db_passwords = cursor.fetchall()
        passwords = {db_password[0]: db_password[1] for db_password in db_passwords}
        return passwords


class SignVault(QWidget):
    font = QFont('Arial', 14)
    passwords = PasswordStorage.fetch_passwords()
    green_background = "background-color: #00FF00;"

    def __init__(self, parent=None):
        super(SignVault, self).__init__(parent)

        self.setWindowTitle("Sign Vault")

        main_layout = QVBoxLayout()
        search_input_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        add_password_layout = QHBoxLayout()
        name_layout = QVBoxLayout()
        password_layout = QVBoxLayout()
        add_password_button_layout = QVBoxLayout()

        # Design of SearchInput
        self.searchInputDefinition = QLabel("Search")
        self.searchInputDefinition.setFont(self.font)
        self.searchInput = QLineEdit("")
        self.searchInput.setReadOnly(False)
        self.searchInput.returnPressed.connect(self.copy_password)

        # Design of SearchDropDown
        self.searchDropDown = QComboBox()
        self.searchDropDown.addItems(self.passwords.keys())
        self.searchDropDown.currentIndexChanged.connect(self.copy_password_from_dropdown)

        # Design CopyButton
        self.searchButton = QPushButton("Copy")
        self.searchButton.clicked.connect(self.copy_password)

        self.searchSuccess = QLabel("")

        # Set Fonts
        self.searchInput.setFont(self.font)
        self.searchDropDown.setFont(self.font)
        self.searchButton.setFont(self.font)
        self.searchSuccess.setFont(self.font)

        # Design Add Service Layout
        self.addNameInputDefinition = QLabel("Service")
        self.addNameInputDefinition.setFont(self.font)
        self.addNameInput = QLineEdit("")
        self.addNameInput.setFont(self.font)
        self.addNameInput.setReadOnly(False)

        self.addPasswordInputDefinition = QLabel("Password")
        self.addPasswordInputDefinition.setFont(self.font)
        self.addPasswordInput = QLineEdit("")
        self.addPasswordInput.setReadOnly(False)
        self.addPasswordInput.setFont(self.font)

        self.addPasswordEmptyLabel = QLabel("")
        self.addPasswordButton = QPushButton("Create")
        self.addPasswordButton.clicked.connect(self.create_password)
        self.addPasswordButton.setFont(self.font)

        # Design Success Message
        self.addSuccess = QLabel("")
        self.addSuccess.setFont(self.font)

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

    def copy_password_from_dropdown(self):
        for password in self.passwords:
            if password == self.searchDropDown.currentText():
                self.copy_text(self.passwords[password])
                return

    @pyqtSlot()
    def copy_password(self):
        for password in self.passwords:
            if self.searchInput.text().lower() in password.lower():
                self.copy_text(self.passwords[password])
                return

    def create_password(self):
        service = self.addNameInput.text()
        password = self.addPasswordInput.text()
        self.save_to_db(service, password)
        self.addNameInput.setText("")
        self.addPasswordInput.setText("")
        self.addSuccess.setText(" Saved!")
        self.addSuccess.setStyleSheet(self.green_background)

    @staticmethod
    @PasswordStorage.db_connect
    def save_to_db(cursor, connection, service, password):
        cursor.execute(f"""INSERT INTO passwords(name, password) VALUES("{service}", "{password}")""")
        connection.commit()

    def copy_text(self, text):
        subprocess.run("clip",
                       text=True,
                       input=text)
        self.searchSuccess.setText(" Copied!")
        self.searchSuccess.setStyleSheet(self.green_background)


def main():
    app = QApplication(sys.argv)
    sign_vault = SignVault()
    sign_vault.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
