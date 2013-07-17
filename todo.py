from bottle import redirect, request, route, post, run
from todo_classes import todo_list, todo_item, run_command, \
    TODO_PATH, TODO_CONFIG

@route('/list')
def list(list_name='task.txt'):
    project = request.query.project or ''
    context = request.query.context or ''
    date = request.query.date or ''
    priority = request.query.priority or ''

    cur_list = todo_list(priority, date, project, context)
    return cur_list.to_html()

@route('/project/:project')
def project(project =''):
    cur_list = todo_list('project')
    return cur_list.to_html()

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

run(host='localhost', port=8080)
