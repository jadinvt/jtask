import subprocess
from bottle import route, run
TODO_PATH = 'bin/todo'
TODO_CONFIG = 'etc/config.todo'
TODO_BASE_COMMAND = '%s -d %s' %(TODO_PATH, TODO_CONFIG)

@route('/list')
def list(list_name='task.txt'):
		
	list = run_command([TODO_PATH, '-d', TODO_CONFIG, 'list'])
	list = list.replace("\n","<br/>")
	html ='<b>List function %s</b><br/>' % list
	return html


@route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name


def run_command(command):
    p = subprocess.check_output(command)
    return p

run(host='localhost', port=8080)
