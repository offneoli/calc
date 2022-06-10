import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from typing import Union, Optional
from operator import add, sub, mul, truediv
from designcalc import Ui_MainWindow

operations = {'+': add, '-': sub, '*': mul, '/': truediv} #Словарь с операциями

error_zero_div = 'Ne nado delit` na nol`'
error_undefined = 'A vot hz pochemy ne rabotaet'


class Calculator(QMainWindow):
    def __init__(self): #работа приложения
        super(Calculator, self).__init__() #работа приложения
        self.ui = Ui_MainWindow() #работа приложения
        self.ui.setupUi(self) #работа приложения
        self.entry_max_len = self.ui.le_entry.maxLength() #Маскимум длины поля

        #----------------------------------------------------Цифры------------------------------------------------------

        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)

        #-----------------------------------------------------Приколюхи-------------------------------------------------

        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_del.clicked.connect(self.clear_entry)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_aboba.clicked.connect(self.negate)
        self.ui.btn_back.clicked.connect(self.backspace)

        #-----------------------------------------------------Операторы-------------------------------------------------

        self.ui.btn_plus.clicked.connect(self.math_operation)
        self.ui.btn_minus.clicked.connect(self.math_operation)
        self.ui.btn_ymnoj.clicked.connect(self.math_operation)
        self.ui.btn_delit.clicked.connect(self.math_operation)

    def add_digit(self): #добавление цифры в поле ввода, принимает текст кнопки и возвращает дырку от бублика
        self.clear_temp_if_equality() #Чистка временного выражения
        self.remove_error() # удаление ошибки
        btn = self.sender() #сигнал нажатия кнопки и передача. в переменной хранится последняя нажатая кнопка
        digit_buttons = ('btn_1', 'btn_2', 'btn_3', 'btn_4', 'btn_5', 'btn_6', 'btn_7', 'btn_8', 'btn_9', 'btn_0') #создание кортежа
        if btn.objectName() in digit_buttons: #Если имя обьекта, которое послала сигнал совпадает с кортежом, то ->
            if self.ui.le_entry.text() == '0': #берем текст из QT обьекта т.е. когда в поле 0, мы заменяем на прожатую кнопку
                self.ui.le_entry.setText(btn.text()) #Поставить текст в QT обьект
            else:
                self.ui.le_entry.setText(self.ui.le_entry.text() + btn.text()) #Иначе добавляем ее в строку

    def add_point(self) -> None: #легче конверт в вещественное чем с ,
        self.clear_temp_if_equality()  # Чистка временного выражения
        if '.' not in self.ui.le_entry.text(): #если нет в поле ввода . , то добавляем))
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')

    def add_temp(self) -> None: #Временное выражение число + знак
        btn = self.sender() #Пункт add_digit
        entry = self.remove_trailing_zeros(self.ui.le_entry.text()) #обрезание нулей

        if not self.ui.lbl_temp.text() or self.get_math_sign() == '=': #проверка на чистоту или есть равенство, то занос текста
            self.ui.lbl_temp.setText(entry + f' {btn.text()} ')
            self.ui.le_entry.setText('0') #очистка поле ввода

    def negate(self): #Отрицание
        self.clear_temp_if_equality()  # Чистка временного выражения
        entry = self.ui.le_entry.text() #Временно
        if '-' not in entry:
            if entry != '0': #Ноль доп.условие
                entry = '-' + entry #добовляем минус
        else:
            entry = entry[1:] #иначе убираем левый символ
        if len(entry) == self.entry_max_len + 1 and '-' in entry: #Если длина строки больше перемен и есть минус, то увеличиваем макс
            self.ui.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.le_entry.setMaxLength(self.entry_max_len) #Дефолт, если норм
        self.ui.le_entry.setText(entry)

    def disable_buttons(self, disable: bool) -> None: #выключение кнопок
        self.ui.btn_calc.setDisabled(disable)
        self.ui.btn_point.setDisabled(disable)
        self.ui.btn_aboba.setDisabled(disable)
        self.ui.btn_delit.setDisabled(disable)
        self.ui.btn_plus.setDisabled(disable)
        self.ui.btn_ymnoj.setDisabled(disable)
        self.ui.btn_minus.setDisabled(disable)
        color = 'color: grey;' if disable else 'color: black'
        self.change_bottuns_color(color)

    def change_bottuns_color(self, css_color: str) -> None: #возвращение
        self.ui.btn_calc.setStyleSheet(css_color)
        self.ui.btn_point.setStyleSheet(css_color)
        self.ui.btn_aboba.setStyleSheet(css_color)
        self.ui.btn_delit.setStyleSheet(css_color)
        self.ui.btn_plus.setStyleSheet(css_color)
        self.ui.btn_ymnoj.setStyleSheet(css_color)
        self.ui.btn_minus.setStyleSheet(css_color)

    #--------------------------------------------------Чистка и ошибки-----------------------------------------------------------------------------------

    def clear_all(self) -> None: #чистка всех полей
        self.remove_error()  # удаление ошибки
        self.ui.le_entry.setText('0') #0 в поле ввода
        self.ui.lbl_temp.clear() #очищение времменого выражения

    def clear_entry(self) -> None: #Чиска, но чуть
        self.remove_error()  # удаление ошибки
        self.clear_temp_if_equality()  # Чистка временного выражения
        self.ui.le_entry.setText('0') #0 в поле ввода

    def clear_temp_if_equality(self) -> None: #Очищение временного при нажатии кнопки
        if self.get_math_sign() == '=':
            self.ui.lbl_temp.clear()

    def backspace(self) -> None: #Удаление одной цифры
        self.remove_error()  # удаление ошибки
        self.clear_temp_if_equality()  # Чистка временного выражения
        entry = self.ui.le_entry.text()
        if len(entry) != 1: #Проверка на глупого
            if len(entry) == 1 and '-' in entry:
                self.ui.le_entry.setText('0')
            else:
                self.ui.le_entry.setText(entry[:-1])
        else:
            self.ui.le_entry.setText('0')

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:#чтобы удалялись незначащие нули и точки
        n = str(float(num)) #флоат обрезает нули т.е. из стринг в флоат
        return n[:-2] if n[-2:] == '.0' else n

    def show_error(self, text: str) -> None:  # показ ошибки
        self.ui.le_entry.setMaxLength(len(text))
        self.ui.le_entry.setText(text)
        self.disable_buttons(True) #выключение кнопок

    def remove_error(self) -> None:  # убирание ошибки
        if self.ui.le_entry.text() in (error_undefined, error_zero_div):
            self.ui.le_entry.setMaxLength(self.entry_max_len)  # возвращение к дефолту
            self.ui.le_entry.setText('0')
            self.disable_buttons(False) #Включить кнопки

    #-------------------------------------------------Получение чего-то из полей ввода--------------------------------------------------------------

    def get_entry_num(self) -> Union[int, float]: #Получение числа из поле ввода \ юнион позволяет возвращять только целое или вещественное
        entry = self.ui.le_entry.text().strip('.') #удаление точки
        return float(entry) if '.' in entry else int(entry) #если точка есть в энтри иначе целое число

    def get_temp_num(self) -> Union[int, float, None]: #Получение числа из временного выражения
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip('.').split()[0] #разделение и получение числа
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]: #Получение знака временного выражения \ возвращяет либо строку, либо ничего
        if self.ui.lbl_temp.text(): #получить текст, то
            return self.ui.lbl_temp.text().strip('.').split()[-1] #разделить по проблеам и вытащить последнее

    #------------------------------------------------------------Счет------------------------------------------------------------------------------

    def calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()
        if temp: #если временно есть, то
            try:
                result = self.remove_trailing_zeros(
                    str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()))
                ) #Обрезаем нули, приводим к строке, оберем оператор, берем числа
                self.ui.lbl_temp.setText(temp + self.remove_trailing_zeros(entry) + ' =') #Занести вычисление в временное поле
                self.ui.le_entry.setText(result) #вывести результат в временное поле
                return result
            except KeyError: #обработка багов
                pass
            except ZeroDivisionError:
                if self.get_temp_num() == '0':
                    self.show_error(error_undefined)
                else:
                    self.show_error(error_zero_div)

    def math_operation(self) -> None:
        btn = self.ui.lbl_temp.text()
        temp = self.ui.lbl_temp.text()
        if not temp: #если в временно нет, то занос
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == '=':
                    self.add_temp()
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f'{btn.text} ')
            else:
                try:
                    self.ui.lbl_temp.setText(self.calculate() + f' {btn.text}')
                except TypeError:
                    pass


if __name__ == "__main__": #работа приложения 205-209
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())