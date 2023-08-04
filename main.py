import pyperclip
import re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import askyesno, showwarning, showerror


import log_reader

VERSION = 0.1
ICONBASE64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAMAAABHPGVmAAAA7VBMVEUAAAAAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9AAa9B5ntWGp9dpl9RIhtPJ0Nvd3d0EddHT19xaj9O2wtqftNgwftKTrtiqvNnAydvtAwW4AAAAP3RSTlMAACpmd1UZKbHt3KCRIswL3TOq/W+ICSvCbdMQTPVcuxh/Qwfkj34RRO72urn+O8qiSzqHdsOyqDwImcuAkFR93IxsAAADjklEQVRo3u2aa1/aMBTGQcuoF1DcnC0quAkIOt3GnLsvBCi9cPn+H2dqk9LGnJA0Ya94XpZfz9+nyXMS0xYKG230rKKEtrYtyyq94v9oBFK2d1Cs3b3ymiD7KC27vAZIpYoY7RuHHByiF6rWDEOOEEevt41C3iC+jnNCeD+9TaoOMMbDFGV7xZ0KkD1ScjT2njQeLJ/YiTHIblxx4ntE44BSHFOQV6Rg6C2FKcU1BCnF5YZeWhGB1NcJSbycmoHYXIg3jS+fmYGcx9UiBjIjWTECaZDn4jOQML7cNAIhT2vgrRFyQYzMWQiJ5DsTEJckkWWMCfy9CYgDPC3aWy4NQMqk1gIwYpsII2mOU9YIzWLZBKQV18IMw58kRvQhNCRj2Ig+xOG3FGrEMbFo0WFnWwrtwQ0TkDYQkmnKiDYEGPaMEV2ICwz7KL7cKpiAkGEP+K3xaenVh0DDHmSMaEJsftppR+mYgFwi/rAvW6MBSJs/7NRIu2AC0uI3+XRH0Ya4nD0d0xr1IcD8jVgjOpAGMH8zHUUXAszfbEfRhJSB+csEUQ9is/8ucDuKHoQGccAPYqtgAiIbRB0IZAQzHUULIh1EHUiLH8TZiyBqQAAjnCBqQFrSQcwPccUrYr1gAlLnG+EFMTcEao28IOaGOOKlvW0CQo3MZIKYF+LwWyM/iDkhDaDHp4J41e12n89Vu91aPghgJAliL3uudn3TUYdARiIE6kNFFQIZCZCAogiBjIRIpI4aBDIyEkJulCA5RiSxIg1ZMbWIJkEQPJ+rBgFx6ChAICN4FATDx6pRGIYZPj1YvZWHlHqAEVALauVOFlLrAUZEIh3NkoV8RKpGvIgOlqwTutVSMJKcDqPDAznIObDXEmi+nHGfpCCf1RmPVnCS0r4M5At/q7VKPqXcy0C+AueZspQHGQj5gzxl+fGNvfVB/DmertPJYo6HqZ52bxjyVP7FItZXGPhQ+HDCGQ6m3GYvl5Nj/m5r2XCjgWDlkkz8GYLn8CNgKly0vl3J9a5T2h4X0PyBdOu40stvnUNZ4EAM6D1Ydyr7ru8oS/GjwURUv3pklSrK21QruR/7CzwSl+/+yLkX/rliT4Kum8dWt1LU+7KgKQDs2G5N+KZbekvUBOfP1srPG+R3kBzKr/adzEcaKhvu38wzalwUJaXy0v/ESd5Qd/pFBal9WdC/f+hV//y9KKpp8+nPRv9T/wDsNlazku+4/gAAAABJRU5ErkJggg=="
STATUS_DEFAULT = {
    "local_cmdr": "",
    "local_logs_read": False,
    "strangers_logs_dir": "",
    "boxel": "",
    "cmdr_was_in_boxel": False,
    "body_count": "",
    "boxel_stats": ""
}
status = STATUS_DEFAULT

def onClick_update_button():
    update_button.configure(state=["disabled"])
    status_text.set("Чтение ваших логов...")
    root.update()
    status["local_cmdr"] = log_reader.read_local_cmdr_logs()
    status["local_logs_read"] = True
    status_text.set("Ваши логи прочитаны.")
    update_button.configure(state=["enabled"])

def onClick_validate_boxel_button():
    text = enter_boxel_entry.get()
    result = re.match("^[A-Za-z\s]+\s[A-Z]{2}-[A-Z]\s[abcdefgh][0-9]+-$", text) is not None
    if not result:
        boxel_error_message.set("Введите субсектор в формате \"Boepp AA-A a0-\"")
    else:
        boxel_error_message.set("")
        status["boxel"] = text
        if status["local_logs_read"] == False:
            if askyesno(title="Прочитать логи?", message="Ваши логи не прочитаны. Без их чтения продолжить невозможно. Сделать это сейчас?"):
                onClick_update_button()
            else:
                return
        if log_reader.check_if_cmdr_was_in_boxel(status["local_cmdr"], status["boxel"]) == False:
            showwarning(title="Внимание.", message="В ваших логах этот субсектор не обнаружен. Поиск будет вестись только по чужим логам.")
        else:
            status["cmdr_was_in_boxel"] = True
        deactivate_all()
        activate_stage_two()

def onClick_choose_directory_button():
    dirpath = filedialog.askdirectory()
    if dirpath != "":
        status["strangers_logs_dir"] = dirpath
        deactivate_all()
        cmdrs_found_counter.set("Чтение логов...")
        status_text.set("Чтение чужих логов...")
        root.update()
        log_reader.read_local_strangers_logs(dirpath, status["local_cmdr"])
        status_text.set("Логи других командиров прочитаны.")
        cmdrs_were_in_boxel_count = log_reader.how_many_cmdrs_were_in_boxel(status["boxel"], status["local_cmdr"])
        if status["cmdr_was_in_boxel"] == False:
            if cmdrs_were_in_boxel_count == 0:
                showerror(title="Субсектор не найден.", message="Субсектор не найден ни в ваших, ни в сторонних логах.")
                cmdrs_found_counter.set("Ожидание выбора папки...")
                deactivate_all()
                activate_stage_one()
                return
            else:
                cmdrs_found_counter.set(f"{cmdrs_were_in_boxel_count} коммандир(а/ов) были в этом субсекторе.")
        else:
            if cmdrs_were_in_boxel_count == 0:
                cmdrs_found_counter.set("Только вы были в этом субсекторе.")
            else:
                cmdrs_found_counter.set(f"{cmdrs_were_in_boxel_count} коммандир(а/ов), помимо вас, были в этом субсекторе.") 
        activate_stage_three()

def onClick_unite_button():
    deactivate_all()
    status_text.set("Объединение логов...")
    result = log_reader.unite_logs(status["boxel"])
    status["body_count"] = result[0]
    status["boxel_stats"] = result[1]
    status_text.set("Логи объединены.")
    success_text.set("Успешно объединено.")
    activate_stage_four()

def onClick_to_beginning_button():
    deactivate_all()
    activate_stage_one()
    status_text.set("Сброшено в начало.")

def deactivate_all():
    enter_boxel_label.configure(foreground="grey")
    enter_boxel_label.update()
    enter_boxel_entry.configure(state=["disabled"])
    validate_boxel_button.configure(state=["disabled"])
    enter_path_label.configure(foreground="grey")
    choose_directory_button.configure(state=["disabled"])
    cmdrs_found_counter_label.configure(foreground="grey")
    unite_button.configure(state=["disabled"])
    update_button.configure(state=["disabled"])
    success_label.configure(foreground="grey")
    copy_body_count_button.configure(state=["disabled"])
    copy_boxel_stats_button.configure(state=["disabled"])
    to_beginning_button.configure(state=["disabled"])
    root.update()

def activate_stage_one():
    status = STATUS_DEFAULT
    enter_boxel_label.configure(foreground="black")
    enter_boxel_entry.configure(state=["enabled"])
    validate_boxel_button.configure(state=["enabled"])
    update_button.configure(state=["enabled"])
    root.update()

def activate_stage_two():
    enter_path_label.configure(foreground="black")
    choose_directory_button.configure(state=["enabled"])
    update_button.configure(state=["enabled"])
    root.update()

def activate_stage_three():
    cmdrs_found_counter_label.configure(foreground="black")
    unite_button.configure(state=["enabled"])
    update_button.configure(state=["enabled"])
    root.update()

def activate_stage_four():
    success_label.configure(foreground="black")
    copy_body_count_button.configure(state=["enabled"])
    copy_boxel_stats_button.configure(state=["enabled"])
    to_beginning_button.configure(state=["enabled"])
    update_button.configure(state=["enabled"])
    root.update()

def onClick_copy_BC_button():
    pyperclip.copy(status["body_count"])
    status_text.set("BodyCount скопирован в буфер обмена.")

def onClick_copy_BS_button():
    pyperclip.copy(status["boxel_stats"])
    status_text.set("BoxelStats скопирован в буфер обмена.")


# основное окно
root = Tk()
root.title(f"LUCAS v{VERSION}")
icon = PhotoImage(data=ICONBASE64)
root.iconphoto(False, icon)
root.geometry("400x400")
root.resizable(False, False)

# 1: поле ввода субсектора
boxel_input_frame = ttk.Frame(borderwidth=3, relief=SOLID, padding=5)
for c in range(2): boxel_input_frame.columnconfigure(index=c, weight=1)
for r in range(3): boxel_input_frame.rowconfigure(index=r, weight=1)
enter_boxel_label = ttk.Label(boxel_input_frame, text="Введите субсектор:")
enter_boxel_label.grid(column=0, row=0, sticky=W)
enter_boxel_entry = ttk.Entry(boxel_input_frame, width=35)
enter_boxel_entry.grid(column=1, row=0, sticky=E)
boxel_error_message = StringVar()
error_message_label = ttk.Label(boxel_input_frame, foreground="red", textvariable=boxel_error_message)
error_message_label.grid(column=1, row=1, sticky=E)
validate_boxel_button = ttk.Button(boxel_input_frame, text="Продолжить", width=20, command=onClick_validate_boxel_button)
validate_boxel_button.grid(column=1, row=2, sticky=E)
boxel_input_frame.pack(side=TOP, fill=X)

# 2: поле ввода директории с чужими логами
logs_path_input_frame = ttk.Frame(borderwidth=3, relief=SOLID, padding=5)
for c in range(2): logs_path_input_frame.columnconfigure(index=c, weight=1)
for r in range(3): logs_path_input_frame.rowconfigure(index=r, weight=1)
enter_path_label = ttk.Label(logs_path_input_frame, text="Выберите папку с чужими логами:", foreground="grey")
enter_path_label.grid(column=0, row=0, sticky=W)
choose_directory_button = ttk.Button(logs_path_input_frame, text="Выбрать папку", width=20, state=["disabled"], command=onClick_choose_directory_button)
choose_directory_button.grid(column=1, row=0, sticky=E)
cmdrs_found_counter = StringVar()
cmdrs_found_counter.set("Ожидание выбора папки...")
cmdrs_found_counter_label = ttk.Label(logs_path_input_frame, textvariable=cmdrs_found_counter, foreground="grey")
cmdrs_found_counter_label.grid(column=0, row=1, columnspan=2, sticky=W)
unite_button = ttk.Button(logs_path_input_frame, text="Объединить логи", width=20, state=["disabled"], command=onClick_unite_button)
unite_button.grid(column=0, columnspan=2, row=2, sticky=E)
logs_path_input_frame.pack(side=TOP, fill=X)

# 3: окно результатов
results_frame = ttk.Frame(borderwidth=3, relief=SOLID, padding=5)
for r in range(3): results_frame.rowconfigure(index=r, weight=1)
for c in range(2): results_frame.columnconfigure(index=c, weight=1)
success_text = StringVar()
success_text.set("Ожидание...")
success_label = ttk.Label(results_frame, textvariable=success_text, foreground="grey")
success_label.grid(row=0, column=0, columnspan=2)
copy_body_count_button = ttk.Button(results_frame, text="Копировать BodyCount", width=30, state=["disabled"], command=onClick_copy_BC_button)
copy_body_count_button.grid(row=1, column=0)
copy_boxel_stats_button = ttk.Button(results_frame, text="Копировать BoxelStats", width=30, state=["disabled"], command=onClick_copy_BS_button)
copy_boxel_stats_button.grid(row=1, column=1)
to_beginning_button = ttk.Button(results_frame, text="В начало", state=["disabled"], command=onClick_to_beginning_button)
to_beginning_button.grid(row=2, column=0, columnspan=2)
results_frame.pack(side=TOP, fill=X)

# нижняя панель
bottom_frame = ttk.Frame(borderwidth=3, relief=SOLID, padding=5)
for c in range(2): bottom_frame.columnconfigure(index=c, weight=1)
status_text = StringVar()
status_text.set("Готов.")
status_label = ttk.Label(bottom_frame, textvariable=status_text)
status_label.grid(column=0, row=0, sticky=W)
update_button = ttk.Button(bottom_frame, text="Прочитать свои логи", command=onClick_update_button)
update_button.grid(column=1, row=0, sticky=E)
bottom_frame.pack(side=BOTTOM, fill=X)

root.mainloop()