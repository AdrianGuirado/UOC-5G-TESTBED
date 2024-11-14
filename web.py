import os
from bottle import route, run, template

FILES_DIR = 'results_files'

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

index_html = '''<h1> web app! By <strong>{{ author }}</strong>.
                </h1><p>Go to <a href="/files">files</a> to see the files.</p>
             '''

@route('/')
def index():
    return template(index_html, author='Adrián Guirado')

@route('/files')
def list_files():
    files = os.listdir(FILES_DIR)
    files_list = "<ul>"
    for file in files:
        files_list += f"<li>{file}</li>"
    files_list += "</ul>"
    return template('<h2>results_files:</h2> {{files_list}}', files_list=files_list)

@route('/name/<name>')
def name(name):
    return template(index_html, author=name)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)