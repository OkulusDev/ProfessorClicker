#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
from time import sleep
import game_ui
from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, QThread, pyqtSignal

money = 0
students = 0
income = 1
university_seats = 100
knowledge = 1
professor_level = 1
levels_labels = {
	1: '2 + x = 4',
	2: '3 - (x + x) = 9',
	3: '23 : 34x * 2z + 3 = ?',
	4: '(x^4 + x^7)^8 + 21x^2y^9 = ?',
	5: '(x^b27 + y^2xb)^bx + 34 * x^2yb^3 = ?'
}


class MoneyWorker(QObject):
	finished = pyqtSignal()
	progress = pyqtSignal(int)

	def run(self):
		global money
		global income
		
		while True:
			sleep(1)
			money += income
			self.progress.emit(money)
		
		self.finished.emit()


class StudentsWorker(QObject):
	finished = pyqtSignal()
	progress = pyqtSignal(int)

	def run(self):
		global professor_level
		global students
		
		while True:
			sleep(1)
			if students > 100 * professor_level:
				professor_level += 1
				self.progress.emit(professor_level)

		self.finished.emit()


class ProfessorClickerUI(QtWidgets.QMainWindow, game_ui.Ui_MainWindow):
	def __init__(self):
		###### Инициализация и установка UI ######
		super().__init__()
		self.setupUi(self)
		self.start_clicker_thread()
		self.start_level_checker()

		self.setFixedSize(719, 704)
		self.setWindowTitle("Professor Clicker Game")

		self.money_label.setText(f'Деньги: {money}$')
		self.income_label.setText(f'Доход: {income}$')
		self.player_lvl.setText(f'Уровень: {professor_level}')
		self.students_label.setText(f'Студенты: {students}/{university_seats}')
		self.knowledge_label.setText(f'Знания: {knowledge}')

		self.player_lvl.setText(f'Уровень: {professor_level}')

		self.takeGoodStudent_btn.clicked.connect(self.take_good_student)
		self.takeMiddleStudent_btn.clicked.connect(self.take_middle_student)
		self.takeBadStudent_btn.clicked.connect(self.take_bad_student)
		self.take_free_student.clicked.connect(self.take_free_student_func)

		self.up_university_ten_btn.clicked.connect(lambda: self.up_university(10, price=100 * professor_level))
		self.up_university_ten_btn.setText(f'{100 * professor_level}$')
		self.label_16.setText(f'+{10 * professor_level} мест в университете')

		self.up_university_ten_hundred_btn.clicked.connect(lambda: self.up_university(100, price=1000 * professor_level))
		self.up_university_ten_hundred_btn.setText(f'{1000 * professor_level}$')
		self.label_17.setText(f'+{100 * professor_level} мест в университете')

		self.up_university_thousand_btn.clicked.connect(lambda: self.up_university(1000, price=10000 * professor_level))
		self.up_university_thousand_btn.setText(f'{10000 * professor_level}$')
		self.label_18.setText(f'+{1000 * professor_level} мест в университете')

		self.simple_course_btn.setText(f'{50 * professor_level}$')
		self.simple_course_btn.clicked.connect(lambda: self.learn_course('simple', 50 * professor_level))

		self.hundred_math_btn.setText(f'{100 * professor_level}$')
		self.hundred_math_btn.clicked.connect(lambda: self.learn_course('basic', 100 * professor_level))

		self.thousand_math_btn.setText(f'{1000 * professor_level}$')
		self.thousand_math_btn.clicked.connect(lambda: self.learn_course('middle', 1000 * professor_level))

		self.five_thousands_math_btn.setText(f'{5000 * professor_level}$')
		self.five_thousands_math_btn.clicked.connect(lambda: self.learn_course('pro', 5000 * professor_level))

		self.takeGoodStudent_btn.setText(f'{100 * professor_level}$')
		self.takeBadStudent_btn.setText(f'{15 * professor_level}$')
		self.takeMiddleStudent_btn.setText(f'{50 * professor_level}$')

	def learn_course(self, course_type, price):
		global money
		global knowledge

		if money >= price:
			money -= price

			if course_type == 'simple':
				knowledge += 1 * professor_level
			elif course_type == 'basic':
				knowledge += 5 * professor_level
			elif course_type == 'middle':
				knowledge += 10 * professor_level
			elif course_type == 'pro':
				knowledge += 50 * professor_level

			self.money_label.setText(f'Деньги: {money}$')
			self.knowledge_label.setText(f'Знания: {knowledge}')
		else:
			print('Не хватает денег')

	def up_university(self, count, price=100):
		global university_seats
		global money

		if money >= price * professor_level:
			money -= 100 * professor_level
			university_seats += count * professor_level
			self.students_label.setText(f'Студенты: {students}/{university_seats}')
		else:
			print('Не хватает денег')

	def take_free_student_func(self):
		global money
		global students
		global income

		if students + 1 * knowledge <= university_seats * professor_level:
			students += 1 * knowledge
			self.students_label.setText(f'Студенты: {students}')
			self.students_label.setText(f'Студенты: {students}/{university_seats}')
		else:
			print('В университете не хватает места')

	def take_bad_student(self):
		global money
		global students
		global income

		if money >= 15 * professor_level and students + 1 * knowledge <= university_seats * professor_level:
			money -= 15
			students += 1 * knowledge
			income += 1 * professor_level
			self.students_label.setText(f'Студенты: {students}')
			self.money_label.setText(f'Деньги: {money}$')
			self.income_label.setText(f'Доход: {income}$')
			self.students_label.setText(f'Студенты: {students}/{university_seats}')
		elif students >= university_seats * professor_level:
			print('В университете не хватает места')
		else:
			print('Не хватает денег')

	def take_middle_student(self):
		global money
		global students
		global income

		if money >= 50 * professor_level and students + 1 * knowledge <= university_seats * professor_level:
			money -= 50
			students += 1 * knowledge
			income += 5 * professor_level
			self.students_label.setText(f'Студенты: {students}')
			self.money_label.setText(f'Деньги: {money}$')
			self.income_label.setText(f'Доход: {income}$')
			self.students_label.setText(f'Студенты: {students}/{university_seats}')
		elif students >= university_seats * professor_level:
			print('В университете не хватает места')
		else:
			print('Не хватает денег')

	def take_good_student(self):
		global money
		global students
		global income

		if money >= 100 * professor_level and students + 1 * knowledge <= university_seats * professor_level:
			money -= 100
			students += 1 * knowledge
			income += 10 * professor_level
			self.students_label.setText(f'Студенты: {students}')
			self.money_label.setText(f'Деньги: {money}$')
			self.income_label.setText(f'Доход: {income}$')
			self.students_label.setText(f'Студенты: {students}/{university_seats}')
		elif students >= university_seats * professor_level:
			print('В университете не хватает места')
		else:
			print('Не хватает денег')

	def update_progress(self, moneys):
		self.money_label.setText(f'Деньги: {moneys}$')

	def update_level(self, level):
		self.player_lvl.setText(f'Уровень: {level}')

		self.takeGoodStudent_btn.setText(f'{100 * professor_level}$')
		self.takeBadStudent_btn.setText(f'{15 * professor_level}$')
		self.takeMiddleStudent_btn.setText(f'{50 * professor_level}$')

		if level < 6:
			pt = 35 - level // 2
			if pt < 20:
				pt = 20
			self.level_label.setStyleSheet(f"font: italic {pt}pt \"Source Code Pro\";\n"
"background: #303039;")
			self.level_label.setText(levels_labels[level])
		else:
			self.level_label.setStyleSheet(f"font: italic 30pt \"Source Code Pro\";\n"
"background: #303039;")
			self.level_label.setText('f(t + dt) = f(t) x e^bxdt')

		self.money_label.setText(f'Деньги: {money}$')
		self.income_label.setText(f'Доход: {income}$')
		self.player_lvl.setText(f'Уровень: {professor_level}')
		self.students_label.setText(f'Студенты: {students}/{university_seats}')
		self.knowledge_label.setText(f'Знания: {knowledge}')

		self.player_lvl.setText(f'Уровень: {professor_level}')

		self.takeGoodStudent_btn.clicked.connect(self.take_good_student)
		self.takeMiddleStudent_btn.clicked.connect(self.take_middle_student)
		self.takeBadStudent_btn.clicked.connect(self.take_bad_student)
		self.take_free_student.clicked.connect(self.take_free_student_func)

		self.up_university_ten_btn.clicked.connect(lambda: self.up_university(10, price=100 * professor_level))
		self.up_university_ten_btn.setText(f'{100 * professor_level}$')
		self.label_16.setText(f'+{10 * professor_level} мест в университете')

		self.up_university_ten_hundred_btn.clicked.connect(lambda: self.up_university(100, price=1000 * professor_level))
		self.up_university_ten_hundred_btn.setText(f'{1000 * professor_level}$')
		self.label_17.setText(f'+{100 * professor_level} мест в университете')

		self.up_university_thousand_btn.clicked.connect(lambda: self.up_university(1000, price=10000 * professor_level))
		self.up_university_thousand_btn.setText(f'{10000 * professor_level}$')
		self.label_18.setText(f'+{1000 * professor_level} мест в университете')

		self.simple_course_btn.setText(f'{50 * professor_level}$')
		self.simple_course_btn.clicked.connect(lambda: self.learn_course('simple', 50 * professor_level))

		self.hundred_math_btn.setText(f'{100 * professor_level}$')
		self.hundred_math_btn.clicked.connect(lambda: self.learn_course('basic', 100 * professor_level))

		self.thousand_math_btn.setText(f'{1000 * professor_level}$')
		self.thousand_math_btn.clicked.connect(lambda: self.learn_course('middle', 1000 * professor_level))

		self.five_thousands_math_btn.setText(f'{5000 * professor_level}$')
		self.five_thousands_math_btn.clicked.connect(lambda: self.learn_course('pro', 5000 * professor_level))

		self.takeGoodStudent_btn.setText(f'{100 * professor_level}$')
		self.takeBadStudent_btn.setText(f'{15 * professor_level}$')
		self.takeMiddleStudent_btn.setText(f'{50 * professor_level}$')

	def start_level_checker(self):
		global professor_level

		self.thread2 = QThread()
		self.worker2 = StudentsWorker()

		self.worker2.moveToThread(self.thread2)
		self.thread2.started.connect(self.worker2.run)
		self.worker2.finished.connect(self.thread2.quit)
		self.worker2.finished.connect(self.worker2.deleteLater)
		self.thread2.finished.connect(self.thread2.deleteLater)
		self.worker2.progress.connect(self.update_level)
		self.thread2.start()

	def start_clicker_thread(self):
		global money
		
		self.thread = QThread()
		self.worker = MoneyWorker()
		
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		self.worker.progress.connect(self.update_progress)
		self.thread.start()


def main():
	app = QtWidgets.QApplication(sys.argv)
	window = ProfessorClickerUI()
	window.show()
	app.exec()


if __name__ == '__main__':
	main()
