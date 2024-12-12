import tkinter as tk

from core.record_service import RecordService
from infrastructure.json_record_repository import JsonRecordRepository
from infrastructure.main_window import MainWindow

def main():
    repository = JsonRecordRepository("records.json")
    record_service = RecordService(repository)
    
    root = tk.Tk()
    app = MainWindow(root, record_service)
    root.mainloop()

if __name__ == "__main__":
    main()