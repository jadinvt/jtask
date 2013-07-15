import subprocess
from bottle import redirect, request, route, post, run
TODO_PATH = 'bin/todo'
TODO_CONFIG = 'etc/config.todo'
TODO_BASE_COMMAND = '%s -d %s' %(TODO_PATH, TODO_CONFIG)

@route('/list')
def list(list_name='task.txt'):
		
	list = run_command([TODO_PATH, '-d', TODO_CONFIG, 'list'])
	list = list.replace("\n","<br/>")
	html = list
    html = 'blah'
    # <input name="task"     type="text" />
    # <input type="submit" />
    # </form>"""
	return html


@post('/add')
def task():
	task = request.forms.get('task')
	if task:
		run_command([TODO_PATH, '-d', TODO_CONFIG, 'a', "%s" % task])
	redirect('/list')

@route('/')
@route('/hello/:name')
def index(name='World'):

    return '''<form method="POST" action="/add">
                <input name="task"     type="text" />
                <input type="submit" />
              </form>'''


def run_command(command):
    p = subprocess.check_output(command)
    return p

run(host='localhost', port=8080)
