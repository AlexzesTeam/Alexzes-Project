from flask import *
import os
import shutil
from ast import literal_eval
from random import randint, choice
import apsw as sql
import smtplib as sm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
temp_dir = os.path.join(BASE_DIR, "templates")
cont_dir = os.path.join(static_dir, "container")
db_dir = os.path.join(static_dir, "db")
imgs_dir = os.path.join(static_dir, "imgs")
DIRS = (cont_dir, db_dir, imgs_dir)
for dir in DIRS:
    if not os.path.exists(dir):
        os.mkdir(dir)
db = sql.Connection(os.path.join(db_dir, "Data.db"))
mydb = db.cursor()
mydb.execute(
    "CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY_KEY, email TEXT, password TEXT, type TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS tosignup(id TEXT PRIMARY_KEY, ver_num TEXT, data TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS schools(id TEXT PRIMARY_KEY, name TEXT, address TEXT, code TEXT, grades TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS teachers(id TEXT PRIMARY_KEY, name TEXT, school_code TEXT, classes TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS students(id TEXT PRIMARY_KEY, name TEXT, class_code TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS grades(code TEXT, name TEXT, school_code TEXT, classes TEXT, subjects TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS classes(code TEXT, name TEXT, school_code TEXT, grade TEXT, students TEXT, teachers TEXT)"
)
mydb.execute(
    "INSERT INTO users VALUES('1', 'school@gmail.com', '12121212', 'sc')",
)
mydb.execute(
    "INSERT INTO users VALUES('2', 'teacher@gmail.com', '12121212', 't')",
)
mydb.execute(
    "INSERT INTO users VALUES('3', 'student@gmail.com', '12121212', 'st')",
)
mydb.execute(
    "INSERT INTO users VALUES('4', 'student2@gmail.com', '12121212', 'st')",
)
mydb.execute(
    """INSERT INTO schools VALUES('1', 'WE', 'Address', 'code_for_we', "['we_g1']")"""
)
mydb.execute(
    """INSERT INTO teachers VALUES('2', 'Abdo', 'code_for_we', "['class_g1_1', 'class_g1_3']")"""
)
mydb.execute(
    "INSERT INTO students VALUES('3', 'Elnagar Ya Negm', 'class_g1_3')"
)
mydb.execute(
    "INSERT INTO students VALUES('4', 'Elnagar Ya Negm 2', 'class_g1_1')"
)
mydb.execute(
    '''INSERT INTO grades VALUES('we_g1', 'Grade 1', 'code_for_we', "['class_g1_1', 'class_g1_2', 'class_g1_3']", "[]")'''
)
mydb.execute(
    '''INSERT INTO classes VALUES('class_g1_1', '1-1', 'code_for_we', 'we_g1', "['4']", "['2']")'''
)
mydb.execute(
    '''INSERT INTO classes VALUES('class_g1_2', '1-2', 'code_for_we', 'we_g1', "[]", "[]")'''
)
mydb.execute(
    '''INSERT INTO classes VALUES('class_g1_3', '1-3', 'code_for_we', 'we_g1', "['3']", "['2']")'''
)
mydb.execute('select * from users')
for i in mydb.fetchall():
    print(i)

