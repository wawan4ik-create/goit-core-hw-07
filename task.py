from collections import UserDict

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

class Record:
    """
    Клас, що представляє запис контакту.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

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


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print(book)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)     # Contact name: John, phones: 1112223333; 5555555555

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")    # John: 5555555555

    book.delete("Jane")
    print(book)     # лише John
    #john.edit_phone("1112223333", "abc")    # ValueError