import sys
import json
from workflow import web
from base import gen_wf, package_list_url, hint


def main(wf):
    app = wf.args[0]
    result = get_package_list(app)
    if result.get('errcode') != 0:
        wf.add_item(title=result.get('errmsg'))
    else:
        package_list = result.get('result')
        for package in package_list:
            wf.add_item(title=package, subtitle=hint, arg='{app} {package}'.format(app=app, package=package), valid=True)
    wf.send_feedback()


def get_package_list(app):
    wf.logger.debug('fetching package list')
    resp = web.get(package_list_url, params={
        'module': app
    })
    resp.raise_for_status()
    return json.loads(resp.content)


if __name__ == '__main__':
    wf = gen_wf()
    sys.exit(wf.run(main))