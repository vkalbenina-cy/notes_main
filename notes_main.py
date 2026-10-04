# приложение с умными заметками
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QLineEdit, QInputDialog, QMessageBox
import json
app = QApplication([])
main_win = QWidget()

main_win.resize(800, 600)
main_win.setWindowTitle('Умные заметки')
#создание виджетов
field_text = QTextEdit()
list_notes_title = QLabel('Список заметок')
list_notes = QListWidget()
btn_create_note = QPushButton('Создать заметку')
btn_delete_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')
list_tags_title = QLabel('Список тегов')
list_tags = QListWidget()
field_tag = QLineEdit()
btn_add_tag = QPushButton('Добавить к заметке')
btn_unpin_tag = QPushButton('Открепить от заметки')
btn_search_tag = QPushButton('Искать заметки по тегу')

field_tag.setPlaceholderText('Введите тег...')

#создание лэйаутов
main_line = QHBoxLayout()
v_line = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line2 = QHBoxLayout()
#добавление виджетов
main_line.addWidget(field_text)
main_win.setLayout(main_line)

v_line.addWidget(list_notes_title)
v_line.addWidget(list_notes)

h_line1.addWidget(btn_create_note)
h_line1.addWidget(btn_delete_note)
v_line.addLayout(h_line1)

v_line.addWidget(btn_save_note)
v_line.addWidget(list_tags_title)
v_line.addWidget(list_tags)
v_line.addWidget(field_tag)

h_line2.addWidget(btn_add_tag)
h_line2.addWidget(btn_unpin_tag)
v_line.addLayout(h_line2)

v_line.addWidget(btn_search_tag)

main_line.addLayout(v_line)
#открытие файла json на чтение
with open('notes.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)

list_notes.addItems(notes)

def show_note():
    title = list_notes.selectedItems()[0].text()#возвращает или задает коллекцию выбранных в текущий момент элементов в компонентах списков, таблиц или деревьев
    text = notes[title]['текст']
    field_text.setText(text)
    list_tags.clear()
    list_tags.addItems(notes[title]['теги'])
list_notes.clicked.connect(show_note)

def add_note():
    title, ok = QInputDialog.getText(main_win, 'Создание заметки', 'Название заметки')
    if ok:
        title = title.strip()
        if title in notes:
           show_error('Ошибка! Такая заметка уже существует.')
        elif title == '':
            show_error('Ошибка! Вы не ввели название заметки.')
        else:
            notes[title] = {'текст': '', 'теги': []}
            list_notes.addItem(title)
            with open('notes.json', 'w', encoding='utf-8') as file:
                json.dump(notes, file, ensure_ascii=False, indent=4)

def del_note():#удаление 
    if len(list_notes.selectedItems()) > 0:
        title = list_notes.selectedItems()[0].text()
        del notes[title]
        list_notes.clear()
        list_notes.addItems(notes)
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)
    else:
        show_error('Ошибка! Вы не обозначили заметку.')

def save_note():
    if len(list_notes.selectedItems()) > 0:
        title = list_notes.selectedItems()[0].text()
        text = field_text.toPlainText()
        notes[title]['текст'] = text
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)
    else:
        show_error('Ошибка! Вы не обозначили заметку.')

def add_tag():
    if len(list_notes.selectedItems()) > 0:
        title = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        tag = tag.strip()
        if tag != '':
            if tag not in notes[title]['теги']:
                notes[title]['теги'].append(tag)
                list_tags.addItem(tag)
                with open('notes.json', 'w', encoding='utf-8') as file:
                    json.dump(notes, file, ensure_ascii=False, indent=4)
                field_tag.clear()
            else:
                show_error('Такой тег уже существует.')
        else:
            show_error('Ошибка! Введите тег.')
    else:
        show_error('Ошибка! Вы не выбрали заметку.')

def unpin_tag():
    if len(list_tags.selectedItems()) > 0:
        title = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[title]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[title]['теги'])
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)
    else:
        show_error('Ошибка! Вы не обозначили тег.')#более подробное описание
def search_notes():
    tag = field_tag.text()
    tag = tag.strip()
    if tag != '':
        if btn_search_tag.text() == 'Искать заметки по тегу':
            btn_search_tag.setText('Сбросить поиск')
            filtered_notes = []
            for note in notes:
                if tag in notes[note]['теги']:
                    filtered_notes.append(note)
            list_notes.clear()
            list_notes.addItems(filtered_notes)
        else:
            btn_search_tag.setText('Искать заметки по тегу')
            list_notes.clear()
            field_tag.clear()
            list_tags.clear()
            field_text.clear()
            list_notes.addItems(notes)
    else:
        show_error('Ошибка! Введите тег.')



def show_error(text):
    message = QMessageBox()#небольшое окно в случае ошибки
    message.setText(text)
    message.exec_()
#отзыв на нажатие на клавишу
btn_create_note.clicked.connect(add_note)
btn_delete_note.clicked.connect(del_note)
btn_save_note.clicked.connect(save_note)
btn_add_tag.clicked.connect(add_tag)
btn_unpin_tag.clicked.connect(unpin_tag)
btn_search_tag.clicked.connect(search_notes)
main_win.show()
app.exec_()
