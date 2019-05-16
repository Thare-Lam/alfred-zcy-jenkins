import sys
import os
import json
from workflow import web
from base import gen_wf, job_url

HOME_PATH = os.environ['HOME']


def main(wf):
    parameters = wf.args[0].split('#')
    app = parameters[0]
    branch = parameters[1]
    do_compile(wf, app, branch)
    wf.send_feedback()


def do_compile(wf, app, branch):
    with open(os.path.join(HOME_PATH, '.zcy_alfred'), 'r') as r:
        auth_info = json.load(r)
        user = auth_info.get('username')
        token = auth_info.get('password')
        if user is None or token is None:
            wf.add_item(title='username or password is empty', subtitle='check file ~/.zcy_alfred')
            return
        compile_data = get_compile_parameters(user, token, app, branch)
        wf.logger.info('compile data: ')
        wf.logger.info(compile_data)
        resp = web.post(job_url, data=compile_data, headers={'Content-Type': 'application/json'})
        resp.raise_for_status()
        result = json.loads(resp.content)
        if result.get('errcode') != 0:
            wf.add_item(title=result.get('errmsg'))
        else:
            job_name = result.get('result').get('job_name')
            build_num = result.get('result').get('build_num')
            wf.add_item(title=get_compile_title(job_name, build_num), subtitle='Press Enter to view detail',
                        arg=get_compile_detail_url(job_name, build_num), valid=True)


def get_compile_parameters(user, token, app, branch):
    return json.dumps({
        'type': 'compile',
        'user': user,
        'token': token,
        'params': {
            'module': app,
            'git_branch': branch
        }
    })


def get_compile_title(job_name, build_num):
    return '{job_name}#{build_num}'.format(job_name=job_name, build_num=build_num)


def get_compile_detail_url(job_name, build_num):
    return 'http://corp.cai-inc.com/jenkins/view/compile/job/{job_name}/{build_num}/console'.format(job_name=job_name, build_num=build_num)


if __name__ == '__main__':
    wf = gen_wf()
    sys.exit(wf.run(main))