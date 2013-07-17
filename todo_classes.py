import re
import subprocess
TODO_PATH = 'bin/todo'
TODO_CONFIG = 'etc/config.todo'
TODO_BASE_COMMAND = '%s -d %s' %(TODO_PATH, TODO_CONFIG)

class todo_item(object):
    """A single todo tiem"""
    def __init__(self, number, task, project='', context='',
    priority='', due_date=''):
        super(todo_item, self).__init__()
        self.task = task
        self.project = project
        self.context = context
        self.priority = priority
        self.due_date = due_date

    def to_html_list(self):
        print "%(priority)s %(due_date)s %(task)s %(project)s %(context)s" \
        % {'priority':self.priority, 'due_date':self.due_date,
        'task':self.task, 'project':self.project, 'context':self.context}
        list_template = """
        <li> %(priority)s %(due_date)s %(task)s 
        <a href="./list?project=%(project)s">%(project)s</a> %(context)s
        </li> 
        """ % {'priority':self.priority, 'due_date':self.due_date,
        'task':self.task, 'project':self.project, 'context':self.context}
        return list_template

class todo_list():
    """A single .txt file of todos"""
    def __init__(self, priority, date, project, context):
        _filter_options = []
        if priority:
            _filter_options.extend(['|', 'grep', '(%s)' % priority])
        if context:
            _filter_options.extend(['|', 'grep', context])
        if project:
            _filter_options.extend(['|', 'grep', '"%s"' % project])
        if date:
            _filter_options.extend(['|', 'grep', date])
        _args = [TODO_PATH, '-p', '-d', TODO_CONFIG, 'list']
        _args.extend(_filter_options)
        print _args
        stdout = run_command(_args)
        lines = stdout.split("\n")
        print lines
        self.tasks=[]
        for line in lines:
            number = re.search(r'(^\d+)', line)
            if number:
                line = line[:number.start()] + line[number.end():]
                number = number.group(1)
            else:
                continue

            project = re.search(r'(\+\w+)', line)
            if project:
                line = line[:project.start()] + line[project.end():]
                project = project.group(1)
            else:
                project = ''

            context = re.search(r'(@\w+)', line)
            if context:
                line = line[:context.start()] + line[context.end():]
                context = context.group(1)
            else:
                context = ''

            date = re.search(r'(\d+-\d+-\d+)', line)
            if date:
                line = line[:date.start()] + line[date.end():]
                date = date.group(1)
            else:
                date = ''

            priority = re.search(r'(\(\w\))', line)
            if priority:
                line = line[:priority.start()] + line[priority.end():]
                priority = priority.group(1)
            else:
                priority = ''

            self.tasks.append(todo_item(number, line, project, 
                context, date, priority))


    def to_html(self):
        html = '<p><ul>'
        for task in self.tasks:

            html += task.to_html_list()
        html += '</ul></p>'
        return html


def run_command(command):
    p = subprocess.check_output(command)
    return p

