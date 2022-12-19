#from msilib import datasizemask
import sqlite3
import pandas as pd
#import models.colddrinks as cd

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()
def create_table():
    c.execute(
        'CREATE TABLE IF NOT EXISTS data(Date TEXT NOT NULL, Name TEXT NOT NULL,Count INTEGER NOT NULL)')


def create(time,name,count):
    c.execute('INSERT INTO data(Date, Name, Count) VALUES (?, ?, ?)', (Date,Name,Count))
    conn.commit()


def read_():
    c.execute('SELECT * FROM data')
    dat = c.fetchall()
    ind = list(map(lambda x:x[0],c.description))
    data= pd.DataFrame(dat,columns=ind)
    return data
    #return dat
def count_():
    c.execute('select Name,sum(Count) from data GROUP BY Name ') 
    t=c.fetchall()
    ti=pd.DataFrame(t,columns=["Name", "Count"])
    return ti
#optional
def csv(d):
    df = pd.DataFrame(d)
    df.index.Name = 'SNo'
    df.to_csv('cold_drinks.csv')
    #st.write('Data is written successfully to csv File.') 
#optional
def excel(d):
    df = pd.DataFrame(d)
    df.index.Name = 'SNo'
    writer = pd.ExcelWriter('cold_drinks.xlsx')
    df.to_excel(writer)
    writer.save()





