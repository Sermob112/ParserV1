from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QThread, QMutex, QWaitCondition
from parserR import ParserR
class ParserThread(QThread):
    message_signal = Signal(str)
    finished_signal = Signal()
    progress_signal = Signal(int)

    def __init__(self, file_name, folder_path_out, mass):
        super().__init__()
        self.file_name = file_name
        self.folder_path_out = folder_path_out
        self.mass = mass
        self.parR = ParserR(self.file_name)
        self.parR.message_signal.connect(self.message_signal.emit)

         # Флаги для управления потоком
        self._is_paused = False
        self._is_stopped = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()
    def run(self):
        # self.message_signal.emit("Начался парсинг")  # Сообщение о начале парсинга

       
      
        try:
            total_elements = len(self.mass) if self.mass else 0
            processed_elements = 0
            if self.mass is not None:
                for i in self.mass:
                    if self._is_stopped:  # Проверяем, не остановлен ли поток
                        break

                    self.mutex.lock()
                    if self._is_paused:  # Если поток приостановлен, ждем
                        self.condition.wait(self.mutex)
                    self.mutex.unlock()
                    try:
                        self.parR.make_link_num(i, self.folder_path_out)
                        self.parR.parse_head()
                        self.parR.get_supplier_links(i)
                        self.parR.documents(i)
                        self.parR.get_result_contracts(i)
                        self.parR.Make_Dock(i)
                
                        self.message_signal.emit(f"Обработан элемент: {i}")
                    except Exception as e:
                        self.message_signal.emit(f"Ошибка при обработке элемента {i}: {e}")

                    # Обновляем прогресс
                    processed_elements += 1
                    progress = int((processed_elements / total_elements) * 100)
                    self.progress_signal.emit(progress)
            else:
                self.message_signal.emit("Выберите файл для парсинга")

            # self.message_signal.emit("Парсинг завершен")
        except Exception as e:
            self.message_signal.emit(f"Ошибка в потоке: {e}")
        finally:
         
            self.finished_signal.emit()  # Сигнал о завершении работы

    def pause(self):
        # Приостанавливаем поток
        self.mutex.lock()
        self._is_paused = True
        self.mutex.unlock()

    def resume(self):
        # Возобновляем поток
        self.mutex.lock()
        self._is_paused = False
        self.condition.wakeAll()
        self.mutex.unlock()

    def stop(self):
        # Останавливаем поток
        self._is_stopped = True
        self.resume() 