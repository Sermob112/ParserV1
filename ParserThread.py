from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QThread, QMutex, QWaitCondition
from parserR import ParserR
from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition
from queue import Queue, Empty



class ParserThread(QThread):
    message_signal = Signal(str)
    finished_signal = Signal()
    item_processed_signal = Signal()

    def __init__(self, file_name, folder_path_out, task_queue: Queue):
        super().__init__()
        self.file_name = file_name
        self.folder_path_out = folder_path_out
        self.task_queue = task_queue
        self.parR = ParserR(self.file_name)
        self.parR.message_signal.connect(self.message_signal.emit)

        self._is_paused = False
        self._is_stopped = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def run(self):
        try:
            while not self._is_stopped:
                self.mutex.lock()
                if self._is_paused:
                    self.condition.wait(self.mutex)
                self.mutex.unlock()

                try:
                    task = self.task_queue.get_nowait()
                except Empty:
                    break  # Все задания выполнены

                try:
                    self.parR.make_link_num(task, self.folder_path_out)
                    self.parR.parse_head()
                    self.parR.get_supplier_links(task)
                    self.parR.other_info()
                    self.parR.get_result_contracts(task)
                    self.parR.Make_Dock(task)

                    self.message_signal.emit(f"Закупка №{task} обработана")
                except Exception as e:
                    self.message_signal.emit(f"Ошибка при обработке элемента {task}: {e}")

                self.item_processed_signal.emit()
                self.task_queue.task_done()

        except Exception as e:
            self.message_signal.emit(f"Ошибка в потоке: {e}")
        finally:
            self.finished_signal.emit()

    def pause(self):
        self.mutex.lock()
        self._is_paused = True
        self.mutex.unlock()

    def resume(self):
        self.mutex.lock()
        self._is_paused = False
        self.condition.wakeAll()
        self.mutex.unlock()

    def stop(self):
        self._is_stopped = True
        self.resume()
