import csv
import os
import re
from os import remove
from pprint import pprint


# запись csv в список
def csv_to_list(in_file):
    with open(in_file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list


# запись списка в csv
def write_to_csv(in_file, lists):
    with open(in_file, "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(lists)


# приводим номера телефонов в нужный вид
def format_phones(in_file, out_file):
    with open(in_file, encoding="utf8") as f:
        text = f.read()

    pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
    fixed_phones = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', text)

    with open(out_file, 'w+', encoding="utf8") as f:
        f.write(fixed_phones)


# приводим имена в нужный вид
def format_names(in_file):
    contact_list = csv_to_list(in_file)
    for c in contact_list:
        split = c[0].split(' ')
        if len(split) > 1:
            c[0] = split[0]
            c[1] = split[1]
            if len(split) > 2:
                c[2] = split[2]
        split = c[1].split(' ')
        if len(split) > 1:
            c[1] = split[0]
            c[2] = split[1]

    return contact_list


# объединяем информацию по ФИ
def merge_data(contacts_list):
    new_contacts_list = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
    unique_names = set()
    for contact in contacts_list[1:]:
        name = " ".join(contact[:2])
        if name in unique_names:
            for new_contact in new_contacts_list:
                if " ".join(new_contact[:2]) == name:
                    for i, v in zip(range(len(contact)-1), contact):
                        if contact[i] not in new_contact or new_contact[i] == '':
                            new_contact[i] = v
                    for c in new_contacts_list:
                        if new_contact[2:] == c[2:]:
                            new_contacts_list.remove(c)
                    new_contacts_list.append(new_contact)
                    break
        else:
            unique_names.add(name)
            new_contacts_list.append(contact)

    return new_contacts_list


if __name__ == "__main__":
    format_phones("phonebook_raw.csv", "fixed_phones.csv")

    fixed_names = format_names("fixed_phones.csv")
    os.remove("fixed_phones.csv")

    merged_contacts_list = merge_data(fixed_names)

    write_to_csv("phonebook.csv", merged_contacts_list)
