import sys
from base import gen_wf, hint
from env_list import run


def main(wf):

    def fun(env):
        wf.add_item(title=env, subtitle=hint, arg='http://corp.cai-inc.com/jenkins/view/{env}'.format(env=env), valid=True)

    keyword = wf.args[0] if len(wf.args) > 0 else None
    run(wf, keyword, fun)


if __name__ == '__main__':
    wf = gen_wf()
    sys.exit(wf.run(main))