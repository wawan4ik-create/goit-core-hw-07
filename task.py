from collections import UserDict
from datetime import datetime, timedelta
from functools import wraps

def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    """
    
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found"
        except IndexError:
            return "Enter the argument for the command"
    return inner


def parse_input(user_input):
    """
    Розбирає введений користувачем рядок на команду та аргументи.
    Повертає кортеж (command, *args).
    """

    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, *args

class Field:
    """
    Клас, що представляє поле контакту.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    """
    Клас, що представляє телефонний номер контакту.
    """

    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits long and contain only numbers.")
        super().__init__(value)

class Birthday(Field):
    """
    Клас, що представляє день народження контакту.
    """

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()    # Перевірка формату дати
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    super().__init__(self.value)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    """
    Клас, що представляє запис контакту.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday if self.birthday else 'N/A'}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        new_phone = Phone(new_phone)
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit is None:
            raise ValueError("Phone number not found.")
        i = self.phones.index(phone_to_edit)
        self.phones[i] = new_phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    """
    Клас, що представляє адресну книгу.
    """

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value
            try:
                next_birthday = birthday.replace(year=today.year)
            except ValueError:
                # February 29 falls on February 28 in non-leap years.
                next_birthday = birthday.replace(year=today.year, day=28)

            if next_birthday < today:
                try:
                    next_birthday = birthday.replace(year=today.year + 1)
                except ValueError:
                    next_birthday = birthday.replace(year=today.year + 1, day=28)

            if (next_birthday - today).days > 7:
                continue

            congratulation_date = next_birthday
            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append({
                "name": record.name.value,
                "birthday": congratulation_date.strftime("%d.%m.%Y"),
            })

        return upcoming_birthdays

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            # реалізація

        elif command == "phone":
            # реалізація

        elif command == "all":
            # реалізація

        elif command == "add-birthday":
            # реалізація

        elif command == "show-birthday":
            # реалізація

        elif command == "birthdays":
            # реалізація

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()