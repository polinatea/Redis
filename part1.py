# Реализовать хранение для каждого пользователя списка настроек текстового сообщения: 
# название шрифта, размер шрифта, цвет шрифта, начертание. Создать оконное приложение, 
# содержащее поле ввода (для ввода настроек пользователя), кнопку (для сохранения настроек), 
# поле ввода (для текста надписи), надпись (содержит форматированный текст из второго поля ввода), 
# раскрывающийся список (для выбора пользователя). Приложение реализует следующие функции:


# (1) При нажатии на кнопку сохраняет в базе данных настройки для пользователя, 
# введенные в первое поле ввода;

# (2) При вводе текста во второе поле ввода отображает этот текст в надписи;

# (3) При выборе имени пользователя из раскрывающегося списка автоматически 
# форматирует текст в надписи в соответствии с настройками выбранного пользователя.


import tkinter as tk
import redis
from tkinter import *
from tkinter import ttk, font
from tkinter.colorchooser import askcolor
from tkinter import messagebox as mb

r = redis.Redis(host='127.0.0.1')

#Функция вывода уже имеющихся в бд пользователей
def combo_input():        
    keys1=r.keys()
    data=[]
    for key1 in keys1:
        data.append(key1.decode("utf-8"))
    return data 

root = tk.Tk()
root.title('Format')

def save():
   # r.set(entry_new_user.get(),entry_font.get(),entry_font_size.get(), entry_color.get(), entry_font_type.get(),ex=20)
  #  r.mset({"username": entry_new_user.get(),"settings":[entry_font.get(),entry_font_size.get(),entry_color.get(),entry_font_type.get()]})
    if (len(entry_new_user.get())!=0):
        settings_str = entry_font.get()+"!+!"+entry_font_size.get()+"!+!"+entry_color.get()+"!+!"+entry_font_type.get()
        r.set(entry_new_user.get(),settings_str, ex=500)
        combo_choose_user['values'] = combo_input()
    else:
        mb.showerror(title="Ошибка", message="Не было введено имя пользователя!")


print("fontfamilies = ", font.families())

def callback(var, var2, var3, var4, var_str):
    # var - name of font
    # var2 - size
    # var3 - color
    # var4 - 
    content=''
    content= (var.get(), int(var2.get()), var4.get())
    entry_msg_out["text"] = var_str.get()
    if (content[0] in font.families()):

        entry_msg_out.configure(font=content, fg=var3.get())

#Функция вывода Настроек уже имеющего пользователя
def apply_settings(event):
    entry_new_user.delete(0, tk.END)
    entry_font.delete(0, tk.END)
    entry_font_size.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_font_type.delete(0, tk.END)
    
    user=combo_choose_user.get()
    otvet=r.get(user).decode("utf-8")
    funct=otvet.split("!+!")
    entry_font.insert(tk.END,funct[0])
    entry_font_size.insert(tk.END,funct[1])
    entry_color.insert(tk.END,funct[2])
    entry_font_type.insert(tk.END,funct[3])

var = StringVar()
var_size = StringVar()
var_color = StringVar()
var_type = StringVar()
var_string = StringVar()

var.set("Arial")
var_size.set("11")
var_color.set("blue")
var_type.set("normal")
var_string.set("something")

var.trace("w", lambda name, index,mode, var=var: callback(var, var_size,var_color, var_type, var_string))
var_size.trace("w", lambda name, index,mode, var=var: callback(var, var_size,var_color, var_type, var_string))
var_color.trace("w", lambda name, index,mode, var=var: callback(var, var_size,var_color, var_type, var_string))
var_type.trace("w", lambda name, index,mode, var=var: callback(var, var_size,var_color, var_type, var_string))
var_string.trace("w", lambda name, index,mode, var=var: callback(var, var_size,var_color, var_type, var_string))


# output msg
label_msg_out= tk.Label(text='Text:',height=3)
label_msg_out.grid(row=0, column=0,rowspan=2,padx=3,pady=2, sticky=tk.W+tk.E)

entry_msg_out = tk.Label(text = 'test',height=3,width=25, anchor="w")
entry_msg_out.grid(row=0,column=1, rowspan=2,sticky=tk.E+tk.W+tk.S+tk.N)

# input msg
label_msg = tk.Label(text='Entry field:')
label_msg.grid(row = 2, column=0,padx=3,sticky=tk.W+tk.E)

entry_msg = tk.Entry(width=25, textvariable=var_string)
entry_msg.grid(row = 2, column = 1, sticky=tk.W+tk.E, padx=[0, 10])

# Settings
label_settings = tk.Label(text='Settings:', font=("Roboto",20, "bold"))
label_settings.grid(row = 3, column=0,columnspan=2, pady=10,sticky=tk.W+tk.N+tk.E)


# font name
label_font_name = tk.Label(root, text='Choose font:', width=25)
label_font_name.grid(row = 4, column=0)


entry_font = tk.Entry(width=25,textvariable=var)
entry_font.grid(row = 5, column = 0,padx=10)
#entry_font.insert(0, "Arial")


# font size
label_font_size = tk.Label(text='Choose font size:', width=25)
label_font_size.grid(row = 6, column=0)

entry_font_size = tk.Entry(width=25, textvariable=var_size)
entry_font_size.grid(row = 7, column = 0)
#entry_font_size.insert(0, "11")

# color
label_color = tk.Label(text='Choose color:', width=25)
label_color.grid(row = 8, column=0)

entry_color = tk.Entry(width=25,textvariable=var_color)
entry_color.grid(row = 9, column = 0)

# font type
label_font_type = tk.Label(text='Choose font type:', width=25)
label_font_type.grid(row = 10, column=0)

entry_font_type = tk.Entry(width=25, textvariable=var_type)
entry_font_type.grid(row = 11, column = 0,padx=10)

# new user name
label_new_user = tk.Label(text='User name:', width=25)
label_new_user.grid(row = 6, column=1,sticky=tk.N+tk.W+tk.E)

entry_new_user = tk.Entry(width=25)
entry_new_user.grid(row = 7, column = 1,padx=10,sticky=tk.N+tk.W+tk.E)

# choose user
label_choose_user = tk.Label(text='Choose user:', width=23)
label_choose_user.grid(row = 8, column=1,sticky=tk.N+tk.W+tk.E)

combo_choose_user=ttk.Combobox(width=23)
combo_choose_user.grid(row=9, column=1,sticky=tk.W+tk.E, padx=7)
combo_choose_user['values'] = combo_input()
combo_choose_user.bind("<<ComboboxSelected>>", apply_settings, combo_input())


save_btn = tk.Button(text='Save', command=save, width=10)
save_btn.grid(row = 12,column=0, pady=20)


root.mainloop()