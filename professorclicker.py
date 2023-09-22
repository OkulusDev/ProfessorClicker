#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
from time import sleep
import game_ui
from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, QThread, pyqtSignal

money = 0
students = 0
income = 10
knowledge = 10
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
		self.students_label.setText(f'Студенты: {students}')
		self.knowledge_label.setText(f'Знания: {knowledge}')

		self.player_lvl.setText(f'Уровень: {professor_level}')

		self.takeGoodStudent_btn.clicked.connect(self.take_good_student)
		self.takeMiddleStudent_btn.clicked.connect(self.take_middle_student)
		self.takeBadStudent_btn.clicked.connect(self.take_bad_student)
		self.take_free_student.clicked.connect(self.take_free_student_func)

	def take_free_student_func(self):
		global money
		global students
		global income

		students += 1 * knowledge
		self.students_label.setText(f'Студенты: {students}')

	def take_bad_student(self):
		global money
		global students
		global income

		if money > 15 * professor_level:
			money -= 15
			students += 1 * knowledge
			income += 1 * professor_level
			self.students_label.setText(f'Студенты: {students}')
			self.money_label.setText(f'Деньги: {money}$')
			self.income_label.setText(f'Доход: {income}$')
		else:
			print('Не хватает денег')

	def take_middle_student(self):
		global money
		global students
		global income

		if money > 50 * professor_level:
			money -= 50
			students += 1 * knowledge
			income += 5 * professor_level
			self.students_label.setText(f'Студенты: {students}')
			self.money_label.setText(f'Деньги: {money}$')
			self.income_label.setText(f'Доход: {income}$')
		else:
			print('Не хватает денег')

	def take_good_student(self):
		global money
		global students
		global income

		if money > 100 * professor_level:
			money -= 100
			students += 1 * knowledge
			income += 10 * professor_level
			self.students_label.setText(f'Студенты: {students}')
			self.money_label.setText(f'Деньги: {money}$')
			self.income_label.setText(f'Доход: {income}$')
		else:
			print('Не хватает денег')

	def update_progress(self, moneys):
		self.money_label.setText(f'Деньги: {moneys}$')

	def update_level(self, level):
		self.player_lvl.setText(f'Уровень: {level}')
		self.level_label.setText(levels_labels[level])

		if level > 3:
			pt = 35 - level // 2
			if pt < 20:
				pt = 20
			self.level_label.setStyleSheet(f"font: italic {pt}pt \"Source Code Pro\";\n"
"background: #303039;")

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
