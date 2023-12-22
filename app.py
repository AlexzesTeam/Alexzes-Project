from flask import *
import os
import shutil
from ast import literal_eval
from random import randint, choice
import apsw as sql
import smtplib as sm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def mk_num():
    lst = [str(i) for i in range(10)]
    x = ""
    last = ""
    for i in range(8):
        d = choice(lst)
        while d == last:
            d = choice(lst)
        x += d
        last = d

    return int(x)


def mk_code():
    mydb.execute("SELECT id FROM users")
    try:
        lst2 = mydb.fetchall()
        lst = []
        for i in lst2:
            lst.append(i[0])
    except:
        lst = []

    print(lst)
    letters1 = tuple([chr(i) for i in range(ord("a"), ord("z") + 1)])
    letters2 = tuple([chr(i) for i in range(ord("A"), ord("Z") + 1)])
    nums = tuple([str(i) for i in range(10)])
    ALL = (letters1, letters2, nums)
    x = ""
    last = ""
    used = []
    for i in range(30):
        tpl = choice(ALL)
        y = choice(tpl)
        while last == tpl or y in used:
            tpl = choice(ALL)
            y = choice(tpl)
        x += y
        last = tpl
        used.append(y)
    if x in lst:
        print(True)
        mk_code()
    else:
        return x


def mk_class_code():
    mydb.execute("SELECT code FROM classes")
    try:
        lst2 = mydb.fetchall()
        lst = []
        for i in lst2:
            lst.append(i[0])
    except:
        lst = []
        
    lst = [str(i) for i in range(10)]
    lst2 = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    x = ""
    last = lst
    for i in range(6):
        tpl = choice([lst, lst2])
        while tpl == last:
            tpl = choice([lst, lst2])
        d = choice(tpl)
        x += d
        last = tpl
    x = "c" + str(hex(ord("c"))).replace("0x", "") + x
    if x in lst:
        mk_class_code()
    else:
        return x


def mk_school_code():
    mydb.execute("SELECT code FROM schools")
    try:
        lst2 = mydb.fetchall()
        lst = []
        for i in lst2:
            lst.append(i[0])
    except:
        lst = []
        
    lst = [str(i) for i in range(10)]
    lst2 = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    x = ""
    last = lst
    for i in range(8):
        tpl = choice([lst, lst2])
        while tpl == last:
            tpl = choice([lst, lst2])
        d = choice(tpl)
        x += d
        last = tpl
    x = "s" + str(hex(ord("s"))).replace("0x", "") + x
    if x in lst:
        mk_school_code()
    else:
        return x


def mk_grade_code():
    mydb.execute("SELECT code FROM grades")
    try:
        lst2 = mydb.fetchall()
        lst = []
        for i in lst2:
            lst.append(i[0])
    except:
        lst = []
    lst = [str(i) for i in range(10)]
    lst2 = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    x = ""
    last = lst
    for i in range(8):
        tpl = choice([lst, lst2])
        while tpl == last:
            tpl = choice([lst, lst2])
        d = choice(tpl)
        x += d
        last = tpl
    x = "g" + str(hex(ord("g"))).replace("0x", "") + x
    
    if x in lst:
        mk_grade_code()
    else:
        return x


def send(email, name, num):
    em = MIMEMultipart()

    body = f"""
{name},

Thank you for choosing our study platform. As part of our security measures, we have generated a verification number for you.

Verification Number: {num}

Please use this number to complete the verification process and ensure the security of your account.

Best Regards,
Alexzes Team
    """
    em.attach(MIMEText(body, "plain"))
    em["From"] = "alexzesteam@gmail.com"
    em["To"] = email
    em["Subject"] = "Account Verification - School in your pocket"

    smtp = sm.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login("alexzesteam@gmail.com", "wxbpywtxhiwqgdwc")
    smtp.sendmail("alexzesteam@gmail.com", email, em.as_string())
    smtp.quit()


def send2(email, name, num):
    em = MIMEMultipart()

    body = f"""
Dear {name},

We received a request to verify your account on our study platform.

Verification Code: {num}

Please use this code to complete the verification process and ensure the security of your account.


Best Regards,
Alexzes Team
    """
    em.attach(MIMEText(body, "plain"))
    em["From"] = "alexzesteam@gmail.com"
    em["To"] = email
    em["Subject"] = "Account Verification - School in your pocket"

    smtp = sm.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login("alexzesteam@gmail.com", "wxbpywtxhiwqgdwc")
    smtp.sendmail("alexzesteam@gmail.com", email, em.as_string())
    smtp.quit()


def save_sc(id, address, email, password, name):
    mydb.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (id, email, password, "sc"))
    mydb.execute(
        "INSERT INTO schools VALUES(?, ?, ?, ?, ?)",
        (id, name, address, mk_school_code(), "[]"),
    )


def save_st(id, c_code, email, password, name):
    mydb.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (id, email, password, "st"))
    mydb.execute("INSERT INTO students VALUES(?, ?, ?)", (id, name, c_code))


def save_t(id, sc_code, email, password, name):
    mydb.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (id, email, password, "t"))
    mydb.execute("INSERT INTO teachers VALUES(?, ?, ?, ?)", (id, name, sc_code, "[]"))


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

app = Flask(__name__, static_folder=static_dir, template_folder=temp_dir)

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
# mydb.execute(
#     "INSERT INTO users VALUES('1', 'school@gmail.com', '12121212', 'sc')",
# )
# mydb.execute(
#     "INSERT INTO users VALUES('2', 'teacher@gmail.com', '12121212', 't')",
# )
# mydb.execute(
#     "INSERT INTO users VALUES('3', 'student@gmail.com', '12121212', 'st')",
# )
# mydb.execute(
#     "INSERT INTO users VALUES('4', 'student2@gmail.com', '12121212', 'st')",
# )
# mydb.execute(
#     """INSERT INTO schools VALUES('1', 'WE', 'Address', 'code_for_we', "['we_g1']")"""
# )
# mydb.execute(
#     """INSERT INTO teachers VALUES('2', 'Abdo', 'code_for_we', "['class_g1_1', 'class_g1_3']")"""
# )
# mydb.execute(
#     "INSERT INTO students VALUES('3', 'Elnagar Ya Negm', 'class_g1_3')"
# )
# mydb.execute(
#     "INSERT INTO students VALUES('4', 'Elnagar Ya Negm 2', 'class_g1_1')"
# )
# mydb.execute(
#     '''INSERT INTO grades VALUES('we_g1', 'Grade 1', 'code_for_we', "['class_g1_1', 'class_g1_2', 'class_g1_3']", "[]")'''
# )
# mydb.execute(
#     '''INSERT INTO classes VALUES('class_g1_1', '1-1', 'code_for_we', 'we_g1', "['4']", "['2']")'''
# )
# mydb.execute(
#     '''INSERT INTO classes VALUES('class_g1_2', '1-2', 'code_for_we', 'we_g1', "['']", "[]")'''
# )
# mydb.execute(
#     '''INSERT INTO classes VALUES('class_g1_3', '1-3', 'code_for_we', 'we_g1', "['3']", "['2']")'''
# )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html')


@app.route("/")
@app.route("/home")
@app.route("/welcome")
def home():
    return render_template("welcome.html")


@app.route("/fetch-acc/<id>")
def fetch(id):
    mydb.execute("SELECT * FROM users WHERE id = ?", (id,))
    try:
        data = mydb.fetchall()[0]
        tp = data[-1]
        id = data[0]
        if tp == "sc":
            return redirect(url_for("school", id=id))
        elif tp == "st":
            mydb.execute("SELECT * FROM students WHERE id = ?", (id,))
            try:
                x = mydb.fetchall()[0]
                c_id = x[-1]
                return redirect(url_for("student", id=id, c_id=c_id))
            except:
                return render_template("404.html", rem=1)
        elif tp == "t":
            return redirect(url_for("teacher", id=id))
    except:
        return render_template("404.html", rem=1)


@app.route("/get-vercode", methods=["POST", "GET"])
def getVerCode():
    num = request.form.get("v-num")
    id = request.form.get("v-error")
    print(num, id)
    mydb.execute("SELECT * FROM tosignup WHERE id = ?", (id,))
    result = mydb.fetchall()
    exist = 0
    print(result)
    for i in result:
        print(i)
        if num == i[1]:
            exist = 1
            data = dict(literal_eval(i[-1]))

    if exist:
        tp = data["t"]
        if tp == "sc":
            save_sc(id, data["a"], data["e"], data["p"], data["n"])
        elif tp == "st":
            save_st(id, data["c_c"], data["e"], data["p"], data["n"])
        elif tp == "t":
            save_t(id, data["s_c"], data["e"], data["p"], data["n"])

    data = {"exist": exist}
    return jsonify(data)


@app.route("/sc/collectdata/signup", methods=["POST", "GET"])
def sc_signup():
    name = request.form.get("sc-name")
    address = request.form.get("sc-address")
    email = request.form.get("sc-email")
    password = request.form.get("sc-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = mydb.fetchall()
    if len(result) == 0:
        num = mk_num()
        per_data = {"n": name, "p": password, "t": "sc", "e": email, "a": address}
        newId = mk_code()
        mydb.execute(
            "INSERT INTO tosignup(id, ver_num, data) VALUES(?, ?, ?)",
            (newId, num, str(per_data)),
        )
        data = {"exist": "0", "error": newId}
        send(email, name, num)
    else:
        data = {"exist": "1", "error": "Invalid E-mail"}
    return jsonify(data)


@app.route("/t/collectdata/signup", methods=["POST", "GET"])
def t_signup():
    name = request.form.get("t-name")
    code = request.form.get("t-code")
    email = request.form.get("t-email")
    password = request.form.get("t-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = mydb.fetchall()
    if len(result) == 0:
        mydb.execute("SELECT * FROM schools WHERE code = ?", (code,))
        result = mydb.fetchall()
        if len(result) == 0:
            num = mk_num()
            per_data = {"n": name, "p": password, "t": "t", "e": email, "s_c": code}
            newId = mk_code()
            mydb.execute(
                "INSERT INTO tosignup(id, ver_num, data) VALUES(?, ?, ?)",
                (newId, num, str(per_data)),
            )
            data = {"exist": "0", "error": newId}
            send(email, name, num)
        else:
            data = {"exist": "1", "error": "Invalid School code"}
    else:
        data = {"exist": "1", "error": "Invalid E-mail"}
    return jsonify(data)


@app.route("/st/collectdata/signup", methods=["POST", "GET"])
def st_signup():
    name = request.form.get("st-name")
    code = request.form.get("st-cls-code")
    email = request.form.get("st-email")
    password = request.form.get("st-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = mydb.fetchall()
    if len(result) == 0:
        mydb.execute("SELECT * FROM classes WHERE code = ?", (code,))
        result = mydb.fetchall()
        if len(result) == 0:
            num = mk_num()
            per_data = {"n": name, "p": password, "t": "st", "e": email, "c_c": code}
            newId = mk_code()
            mydb.execute(
                "INSERT INTO tosignup(id, ver_num, data) VALUES(?, ?, ?)",
                (newId, num, str(per_data)),
            )
            data = {"exist": "0", "error": newId}
            send(email, name, num)
        else:
            data = {"exist": "1", "error": "Invalid Class code"}
    else:
        data = {"exist": "1", "error": "Invalid E-mail"}
    return jsonify(data)


@app.route("/collectdata/login", methods=["POST", "GET"])
def login():
    email = request.form.get("l-email")
    password = request.form.get("l-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    id = 0
    result = mydb.fetchall()
    for i in result:
        if password == i[2]:
            id = str(i[0])
    print(result)
    data = {"id": id}
    return jsonify(data)


@app.route("/sc/<id>")
def school(id):
    mydb.execute("SELECT * FROM schools WHERE id = ?", (id,))
    try:
        data = mydb.fetchall()[0]
        print(data)
        grades = literal_eval(data[4])
        name = data[1]
        name = name.capitalize()
        spName = name.split()
        if not "School" in spName:
            name += " School"
        address = data[2]
        code = data[3]
        g_data = []
        cTtl = "No grades added... Add to show"
        total_classes = 0
        total_students = 0
        if len(grades) > 0:
            for i in grades:
                mydb.execute("SELECT * FROM grades WHERE code = ?", (i,))
                res = list(mydb.fetchall()[0])
                classes = literal_eval(res[3])
                c_count = len(classes)
                total_classes += c_count
                students = 0
                if c_count > 0:
                    for j in classes:
                        mydb.execute(
                            "SELECT id FROM students WHERE class_code = ?", (j,)
                        )
                        res2 = mydb.fetchall()
                        print(res2)
                        st_count = len(res2)
                        students += st_count
                        total_students += st_count
                url = f'/sc/grade/{ i }/{ id }'
                res.append(c_count)
                res.append(students)
                res.append(url)
                g_data.append(res)
        print(g_data)
        lst = [
            ("Grades :", len(grades)),
            ("Classes :", total_classes),
            ("Students :", total_students),
            ("Code :", code),
        ]

        return render_template(
            "sc_t_st.html",
            sc=True,
            name=name,
            address=address,
            cards=g_data,
            cards_ttl=cTtl,
            id=id,
            lst=lst,
            frm="Grade",
            url_new_g=f"/newGrade/{ code }",
            frm_id='form'
        )

    except IndexError:
        return render_template("404.html", rem=True)


@app.route("/newClass/<sc_code>/grade/<gradeid>/", methods=["POST"])
def newClass(sc_code, gradeid):
    name = request.form.get("g_name")
    try:
        mydb.execute("SELECT * FROM schools WHERE code = ?", (sc_code,))
        school = mydb.fetchall()[0]
        sc_grades = literal_eval(school[4])
        if not gradeid in sc_grades:
            data = {"exist": "1", "error": "Not Found"}
            print(data)
            return jsonify(data)
        mydb.execute("SELECT * FROM grades WHERE code = ?", (gradeid,))
        grade = mydb.fetchall()[0]
        classes = list(literal_eval(grade[-2]))
        new = mk_class_code()
        classes.append(str(new))
        mydb.execute(
            "UPDATE grades SET classes = ? WHERE code = ?", (str(classes), gradeid)
        )
        mydb.execute(
            "INSERT INTO classes VALUES(?, ?, ?, ?, ?, ?)",
            (new, name, sc_code, gradeid, "[]", "[]"),
        )
        data = {"exist": "0"}
    except:
        data = {"exist": "1", "error": "Internal Server Error"}
    return jsonify(data)

@app.route("/newGrade/<sc_code>", methods=["POST"])
def newGrade(sc_code):
    name = request.form.get("g_name")
    mydb.execute("SELECT * FROM schools WHERE code = ?", (sc_code,))
    try:
        sc = mydb.fetchall()[0]
        grades = list(literal_eval(sc[-1]))
        new = mk_grade_code()
        grades.append(str(new))
        mydb.execute(
            "UPDATE schools SET grades = ? WHERE code = ?", (str(grades), sc_code)
        )
        mydb.execute(
            "INSERT INTO grades VALUES(?, ?, ?, ?, ?)",
            (new, name, sc_code, "[]", "[]"),
        )
        data = {"exist": "0"}
    except:
        data = {"exist": "1", "error": "Internal Server Error"}
    return jsonify(data)


@app.route("/sc/grade/<gradeid>/<id>")
def sc_grade(id, gradeid):
    try:
        mydb.execute("SELECT * FROM grades WHERE code = ?", (gradeid,))
        g_data = mydb.fetchall()[0]
        mydb.execute("SELECT * FROM schools WHERE id = ?", (id,))
        s_data = mydb.fetchall()[0]
        sc_grades = literal_eval(s_data[4])
        if not gradeid in sc_grades:
            print('Not Found')
            return render_template("404.html")
    except:
        return render_template("404.html")
    c_data = []
    classes = list(literal_eval(g_data[3]))
    total_s = 0
    if len(classes) > 0:
        for i in classes:
            mydb.execute("SELECT * FROM classes WHERE code = ?", (i,))
            res = list(mydb.fetchall()[0])
            url = f'/sc/grade/{ gradeid }/class/{ i }/{ id }'
            x = list(literal_eval(res[4]))
            students = len(x)
            total_s += students
            res.append(students)
            res.append(url)
            print(res)
            c_data.append(res)

    print(classes)
    lst = [("Classes :", len(classes)), ("Students :", total_s)]
    sc_name = s_data[1]
    sc_name = sc_name.capitalize()
    spsc_name = sc_name.split()
    if not "School" in spsc_name:
        sc_name += " School"
    path = [(sc_name, f'/sc/{ id }'), ('>'), (g_data[1], f'/sc/grade/{ gradeid }/{ id }')]
    return render_template(
        "sc_t_st.html", frm="Class", path=path, name=g_data[1], lst=lst, cards=c_data,
        c=True, frm_id='form_class', url_new_g=f'/newClass/{ s_data[3] }/grade/{ gradeid }/'
    )


@app.route("/sc/grade/<gradeid>/class/<classid>/<id>")
def sc_class(id, gradeid, classid):
    return render_template("class.html", sc=True)


@app.route("/t/<id>")
def teacher(id):
    mydb.execute("SELECT * FROM teachers WHERE id = ?", (id,))
    try:
        data = mydb.fetchall()[0]
        return render_template("sc_t_st.html", t=True)
    except:
        return render_template("404.html", rem=True)


@app.route("/t/class/<classid>/<id>")
def t_class(id, classid):
    return render_template("class.html", teacher=True)


@app.route("/st/<id>/c/<c_id>")
def student(id, c_id):
    try:
        mydb.execute("SELECT * FROM students WHERE id = ?", (id,))
        data = mydb.fetchall()[0]
        mydb.execute("SELECT * FROM classes WHERE id = ?", (c_id,))
        c_data = mydb.fetchall()[0]
        return render_template("sc_t_st.html", st=True)
    except:
        return render_template("404.html", rem=True)


@app.route("/st/c/<c_id>/<id>/sub")
def st_subjects(id):
    return render_template("subject.html", student=True)


if __name__ == "__main__":
    app.run(debug=1)
