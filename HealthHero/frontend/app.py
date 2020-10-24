#from flask import Flask, render_template
# 
# app = Flask(__name__)
# 
# 
# @app.route('/')
# def index():
#     return render_template('login.html')
# 
# 
# @app.route('/')
# def index():
#     return render_template('login.html')
# 
# 
# @app.route('/')
# def index():
#     return render_template('login.html')
# 
# 
# @app.route('/')
# def index():
#     return render_template('login.html')
# 
# 
# @app.route('/')
# def index():
#     return render_template('login.html')
# 
# 
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, copy_current_request_context


app = Flask(__name__)
app.secret_key = 'Temp1234'


# Check if user logged in



@app.route('/', methods=['GET', 'POST'])

def slide():
    return render_template('slide.html')


@app.route('/correct', methods=['GET', 'POST'])

def correct():
    return render_template('correct.html')

@app.route('/wrong_explain', methods=['GET', 'POST'])

def wrong_explain():
    return render_template('wrong_explain.html')

@app.route('/search_and_display', methods=['GET', 'POST'])

def search_and_display():
    return render_template('search_and_display.html')


@app.route('/search_content', methods=['GET', 'POST'])

def search_content():
    flash('test complete', 'success')
    return  render_template('search_and_display.html')

@app.route('/upload_file', methods=['GET', 'POST'])

def upload_file():
    return


if __name__ == '__main__':

   app.run(debug=True, port=5001)
  # app.run(debug=True, host='147.128.12.217', port=8080)
