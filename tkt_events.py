from bs4 import BeautifulSoup
import requests
import sqlite3
import tkinter as tk

# defining variables
url = 'https://tkt.ge/event'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
results = soup.find_all(class_='eventItem__EventItemDescTitle-sc-1xt5420-6 geviHq')
satauri = []
pasebi = []
adgili = []
tarigebi = []
koncertebi = []

# scrapping details
for result in results:
    satauri.append(result.text)

result_fasebi = soup.find_all(class_='eventItem__EventItemPrice-sc-1xt5420-9 fUkWwN')

for fasi in result_fasebi:
    pasebi.append(fasi.text)

result_adgili = soup.find_all(class_='eventItem__EventItemDescLocation-sc-1xt5420-7 elQKfu')

for i in result_adgili:
    adgili.append(i.text)

result_date = soup.find_all(class_='eventItem__EventItemDate-sc-1xt5420-4 eQoHvZ')
for result in result_date:
    tarigebi.append(result.text)



for a, b, c in zip(satauri, pasebi, adgili):
    koncertebi.append([a, b, c])


# function for extracting data from sqlite database
def all_from_sql():
    connection = sqlite3.connect('events.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM eventebi')
    data = cursor.fetchall()
    connection.close()
    return data

# creating sqlite table and selecting everything from that database

conn = sqlite3.connect('events.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS eventebi (
                    sataurebi TEXT,
                    fasi INTEGER,
                    adgili TEXT
                    )''')
conn.commit()
cursor.execute('SELECT * FROM eventebi')
conn.commit()
data = cursor.fetchall()
sql_items = [item for item in data]

# comparing python list items with sql database items, if there are new ones adding them
for item in koncertebi:
    if tuple(item) not in list(sql_items):
        print("found new record")
        cursor.execute('INSERT INTO eventebi VALUES (?, ?, ?)', (item[0], item[1], item[2]))
        conn.commit()
    else:
        print("no new records")



# making tkinter window
mainWindow = tk.Tk()
mainWindow.title('TKT.GE')
mainWindow.geometry('1024x768')


names_frame = tk.Frame(mainWindow)
names_frame.pack(fill='both', expand=True)
scrollbar = tk.Scrollbar(names_frame)
scrollbar.pack(side='right', fill='y')
listbox = tk.Listbox(names_frame, yscrollcommand=scrollbar.set, width=60)
listbox.pack(side='left', fill='both', expand=True)
scrollbar.config(command=listbox.yview)

# adding items from sql into tkinter window
everything_fromsql = all_from_sql()

for i in everything_fromsql:
    listbox.insert('end', i)


mainWindow.mainloop()


