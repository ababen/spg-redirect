from flask import Flask, request, render_template, redirect, g
from sqlite3 import OperationalError
import sqlite3

from math import floor
import string
try:
    from urllib.parse import urlparse  # Python 3
    str_encode = str.encode
except ImportError:
    from urlparse import urlparse  # Python 2
    str_encode = str
try:
    from string import ascii_lowercase
    from string import ascii_uppercase
except ImportError:
    from string import lowercase as ascii_lowercase
    from string import uppercase as ascii_uppercase
import base64


# Assuming urls.db is in your app root folder
app = Flask(__name__)
host = 'https://spg-redirect.herokuapp.com/'

'''
def table_check():
    create_table = """
        CREATE TABLE WEB_URL(
        ID INT PRIMARY KEY AUTOINCREMENT,
        URL TEXT NOT NULL,
        TIMES INT NOT NULL
        );
        """
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table)
        except OperationalError:
            pass
'''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('urls.db')
    return db


'''
def toBase62(num, b=62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + ascii_lowercase + ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res

def toBase10(num, b=62):
    base = string.digits + ascii_lowercase + ascii_uppercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res
'''
'''
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = str_encode(request.form.get('url'))
        times = request.form.get('times')
        if urlparse(original_url).scheme == '':
            url = 'https://' + original_url
        else:
            url = original_url
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(
                'INSERT INTO WEB_URL (URL, TIMES) VALUES (?, ?)',
                [base64.urlsafe_b64encode(url), times]
            )
            encoded_string = toBase62(res.lastrowid)
        return render_template('home.html', short_url=host + encoded_string)
    return render_template('home.html')
'''



def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchone()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if urlparse(original_url).scheme == '':
            url = 'https://' + original_url
        else:
            url = original_url
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(
                'INSERT INTO WEB_URL (URL) VALUES (?, ?)', [url])
        return render_template('home.html', short_url=host + encoded_string)
    return render_template('home.html')
'''

@app.route('/<short_url>')
def redirect_short_url(short_url):
    # decoded = toBase10(short_url)
    url = host  # fallback if no URL is found
    try:
        result = query_db('SELECT * FROM RISP WHERE FILENO=?', [short_url])
        if result is not None and result[2] < 1:
            url = 'https://www.spglawfirm.com/risperdal-message'
            with sqlite3.connect('urls.db') as conn:
                        value1 = int(result[2]) + 1
                        value2 = result[1]
                        cursor = conn.cursor()
                        cursor.execute('UPDATE RISP SET USED = ? WHERE FILENO = ?', (value1, value2))
        elif result is None:
            message = 'We are not able to locate your case'
            url = 'error.html'
            return redirect(url, Response=message)
        else:
            print('This URL has already been used.')
            url = 'https://www.spglawfirm.com/risperdal-message-thank-you/'
        return redirect(url)
    except Exception as e:
        print(e)
    return redirect(url)

    '''    
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute('SELECT * FROM RISP WHERE FILENO=?', [short_url])
        short = res.fetchone()

        try:
            # short = res.fetchone()
            if short is not None:
                url = 'https://www.google.com'
        except Exception as e:
            print(e)
        return redirect(url)
    '''

# http://127.0.0.1:5000/148542


if __name__ == '__main__':
    # This code checks whether database table is created or not
    # table_check()
    # app.run(debug=True)
    app.run(host=host)