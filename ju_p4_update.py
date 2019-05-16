import sys
import os
import json
from workflow import web
from base import gen_wf, job_url

HOME_PATH = os.environ['HOME']
jenkins_test = 'jenkins_test'


def main(wf):
    app = wf.args[0]
    package = wf.args[1]
    env = wf.args[2]
    do_update(wf, app, package, env)
    wf.send_feedback()


def do_update(wf, app, package, env):
    with open(os.path.join(HOME_PATH, '.zcy_alfred'), 'r') as r:
        auth_info = json.load(r)
        if is_test_env(env) and jenkins_test in auth_info:
            auth_info = auth_info.get(jenkins_test, {})
        user = auth_info.get('username', None)
        token = auth_info.get('password', None)
        if user is None or token is None:
            wf.add_item(title='username or password is empty', subtitle='check file ~/.zcy_alfred')
            return
        update_data = get_update_parameters(user, token, app, package, env)
        wf.logger.info('update data: ')
        wf.logger.info(update_data)
        resp = web.post(job_url, data=update_data, headers={'Content-Type': 'application/json'})
        resp.raise_for_status()
        result = json.loads(resp.content)
        if result.get('errcode') != 0:
            wf.add_item(title=result.get('errmsg'))
        else:
            job_name = result.get('result').get('job_name')
            build_num = result.get('result').get('build_num')
            wf.add_item(title=get_update_title(job_name, build_num), subtitle='Press Enter to view detail',
                        arg=get_update_detail_url(env, job_name, build_num), valid=True)


def is_test_env(env):
    return 'test' in env


def get_update_parameters(user, token, app, package, env):
    return json.dumps({
        'type': 'update',
        'user': user,
        'token': token,
        'params': {
            'module': app,
            'select_package': package,
            'env': env
        }
    })


def get_update_title(job_name, build_num):
    return '{job_name}#{build_num}'.format(job_name=job_name, build_num=build_num)


def get_update_detail_url(env, job_name, build_num):
    return 'http://corp.cai-inc.com/jenkins/view/{env}/job/{job_name}/{build_num}/console'.format(env=env, job_name=job_name, build_num=build_num)


if __name__ == '__main__':
    wf = gen_wf()
    sys.exit(wf.run(main))