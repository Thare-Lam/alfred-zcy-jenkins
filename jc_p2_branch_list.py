import sys
import json
from workflow import web
from base import gen_wf, branch_list_url, hint


def main(wf):
    app = wf.args[0]
    keyword = wf.args[1] if len(wf.args) > 1 else None
    try:
        branch_list = get_branch_list(wf, app)
        if keyword is not None:
            branch_list = filter(lambda x: keyword in x, branch_list)
        for branch in branch_list:
            wf.add_item(title=branch, subtitle=hint, arg=get_arg(app, branch), valid=True)
    except:
        pass
    wf.send_feedback()


def get_branch_list(wf, app):
    resp = web.get(branch_list_url, params={
        'module': app
    })
    resp.raise_for_status()
    result = json.loads(resp.content)
    if result.get('errcode') != 0:
        wf.add_item(title=result.get('errmsg'))
        raise Exception
    else:
        return result.get('result')


def get_arg(app, branch):
    return '{app}#{branch}'.format(app=app, branch=branch)


if __name__ == '__main__':
    wf = gen_wf()
    sys.exit(wf.run(main))