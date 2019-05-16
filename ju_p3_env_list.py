import sys
from base import gen_wf, hint
from env_list import run


def main(wf):
    app = wf.args[0]
    package = wf.args[1]
    keyword = wf.args[2] if len(wf.args) > 2 else ''

    def fun(env):
        wf.add_item(title=env, subtitle=hint,
                    arg='{app} {package} {env}'.format(app=app, package=package, env=env), valid=True)

    run(wf, keyword, fun)


if __name__ == '__main__':
    wf = gen_wf()
    sys.exit(wf.run(main))