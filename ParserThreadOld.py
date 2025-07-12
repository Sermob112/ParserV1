from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QThread, QMutex, QWaitCondition
from ParserOldR import ParserOldR



class ParserThreadOld(QThread):
    message_signal = Signal(str)
    finished_signal = Signal()
    item_processed_signal = Signal()

    def __init__(self, file_name, folder_path_out, task_queue):
        super().__init__()
        self.file_name = file_name
        self.folder_path_out = folder_path_out
        self.task_queue = task_queue
        self._is_stopped = False
        self._is_paused = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def run(self):
        try:
            while not self.task_queue.empty() and not self._is_stopped:
                self.mutex.lock()
                if self._is_paused:
                    self.condition.wait(self.mutex)
                self.mutex.unlock()

                try:
                    task = self.task_queue.get_nowait()
                except:
                    break

                parser = ParserOldR(self.file_name)
                try:
                    parser.make_link_num(task, self.folder_path_out)
                    parser.parse_head()
                    parser.make_doc()
                    self.message_signal.emit(f"Закупка №{task} обработана")
                except Exception as e:
                    self.message_signal.emit(f"Ошибка при обработке {task}: {e}")

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
