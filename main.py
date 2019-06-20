# Casusgroep 12 - Alain Lardinois & Peter Roijen
import sqlite3
import os
import time


class SqliteDBConnection:
    def __init__(self, type_db):
        self.connect_to_db = sqlite3.connect(type_db)
        self.cursor = self.connect_to_db.cursor()

    def execute_query(self, input_query, *arg):
        self.cursor.execute(input_query, arg)
        return self.cursor.fetchall()

    def modify_table_values(self, modify_value_query, *arg):
        self.cursor.execute(modify_value_query, arg)


class Login(SqliteDBConnection):
    def __init__(self):
        self.login_db_path = os.path.join(os.path.dirname(__file__), 'login_db.db')
        super().__init__(self.login_db_path)
        self.find_user = "SELECT * FROM users WHERE username = ? AND password = ? AND type_user = ?"
        self.logged_in = False

    def search_user(self, type_user, username, password):
        self.logged_in = True
        return self.execute_query(self.find_user, username, password, type_user)


class SPA(SqliteDBConnection):
    def __init__(self, type_user, user_id):
        self.spa_db_path = os.path.join(os.path.dirname(__file__), 'spa_data.db')
        super().__init__(self.spa_db_path)
        self.choice_menu = {1: {1: self.test,
                                0: self.close_program},
                            2: {0: self.close_program},
                            3: {0: self.close_program}}
        self.choice_app = []
        self.user_type = type_user
        self.userID = user_id
        self.done_with_app = False

    def display_menu(self):
        if self.user_type is 1:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. test"
                  "0. Sluit de applicatie af")
            self.choice_app = [1, 0]
        if self.user_type is 2:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. niets 1"
                  "0. Sluit de applicatie af")
            self.choice_app = [1, 0]
        if self.user_type is 3:
            print("\nKies een van de onderstaande taken die u wilt uitvoeren.\n"
                  "1. niets 2"
                  "0. Sluit de applicatie af")
            self.choice_app = [1, 0]

    def app_choice(self):
        valid_menu_choice = False
        while not valid_menu_choice:
            try:
                self.display_menu()
                choice_app = int(input("\nWat is uw keuze?: "))
                if choice_app in self.choice_app:
                    action = self.choice_menu[self.user_type].get(choice_app)
                    action()
                    valid_menu_choice = True
                else:
                    print("\n{} is geen geldige keuze, probeer het nog eens.".format(choice_app))
            except ValueError:
                print("\nU heeft een ongeldig karakter ingevuld, probeer het nog eens.")

    def test(self):
        print("test")

    def close_program(self):
        print("\nU wordt nu uitgelogd. Wij wensen u een fijne dag!")
        time.sleep(2)
        self.done_with_app = True


def login(choice_user, username, password):
    login_user = Login()
    users = login_user.search_user(choice_user, username, password)
    print(users)
    if len(users) > 0:
        print("\nWelkom {} {}.".format(users[0][2], users[0][3]))
        return users
    else:
        print("\nDe opgegeven credentials zijn niet bekend in het systeem, probeer het nog eens.")


def user_credentials():
    print("\nKies een van de onderstaande opties.\n"
          "1. Inloggen student\n"
          "2. Inloggen SLB'er\n"
          "3. Inloggen management\n"
          "0. Applicatie afsluiten")
    while True:
        try:
            choice_user = int(input("\nWat is uw keuze?: "))
            if choice_user is 0:
                return choice_user
            else:
                username = input("\nWat is uw gebruikersnaam?: ")
                password = input("Wat is uw wachtwoord?: ")
                return choice_user, username, password
        except ValueError:
            print("De keuze dat u heeft gemaakt is niet mogelijk, probeer het nog eens.")


def main():
    login_user = Login()

    while not login_user.logged_in:
        credentials = user_credentials()
        if credentials == 0:
            login_user.logged_in = True
        else:
            check_if_logged_in = login(credentials[0], credentials[1], credentials[2])
            use_apps = SPA(credentials[0], check_if_logged_in)
            while not use_apps.done_with_app:
                use_apps.app_choice()


if __name__ == "__main__":
    main()
