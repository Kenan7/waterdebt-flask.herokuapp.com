from flask import Flask, render_template, request, url_for
import urllib.request
import json
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
@app.route('/')
def function():
    return render_template('index.html')

@app.route('/waterdebt', methods=['POST', 'GET'])
def waterdebt():
    error = None
    
    abkodu = request.form['abkodu']

    api_url = "https://opendata.e-gov.az/api/v1/json/azersu/DebtInfo/{}".format(abkodu)
    
    with urllib.request.urlopen(api_url) as url:
        output = url.read().decode('utf-8')
        data = json.loads(output)

    html = data['Response']['HtmlField']
    soup = BeautifulSoup(html, "html.parser")
    l = []

    for a in soup.find_all('b'):
        l.append(re.sub(r"[<b>,</b>]","",str(a)))
          
    return render_template('index.html',
    error=error,
    code = l[1],
    name = l[3],
    debt = l[5])

if __name__ == '__main__':
    app.run()
