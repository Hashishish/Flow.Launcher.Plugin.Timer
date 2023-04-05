import sys
import os
import datetime
from datetime import datetime, timedelta
from flowlauncher import FlowLauncher
from win10toast import ToastNotifier

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))


class Timer(FlowLauncher):

    def query(self, query: str):
        if query.startswith('timer'):
            try:
                # Получаем введенное пользователем время в формате "минуты:секунды"
                time_input = query.split()[1]
                minutes, seconds = map(int, time_input.split(':'))
                # Вызываем метод start_timer с передачей количества секунд
                self.start_timer(minutes * 60 + seconds)
            except:
                self.show_notification('Неверный формат запроса, пожалуйста, попробуйте еще раз')

    def start_timer(self, seconds: int):
        # Получаем время окончания таймера
        end_time = datetime.now() + timedelta(seconds=seconds)
        while datetime.now() < end_time:
            # Вычисляем оставшееся время в секундах
            remaining = (end_time - datetime.now()).seconds
            # Формируем сообщение с оставшимся временем
            message = f'Осталось {remaining // 60} минут и {remaining % 60} секунд'
            # Обновляем прогресс бар и сообщение
            self.update_progress(remaining / seconds, message)
        # По истечению времени вызываем метод для показа уведомления
        self.show_toast_notification('Время таймера истекло!')

    def show_toast_notification(self, message: str):
        # Создаем экземпляр класса ToastNotifier
        toaster = ToastNotifier()
        # Вызываем метод show_toast для создания уведомления
        toaster.show_toast('Таймер', message, duration=10)


if __name__ == '__main__':
    # Создаем экземпляр класса Timer и запускаем его
    Timer()
