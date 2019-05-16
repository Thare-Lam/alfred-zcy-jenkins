from workflow import Workflow3

root_url = 'http://ipaas-test.cai-inc.com/jenkins/api/'

app_list_url = root_url + 'modules'
branch_list_url = root_url + 'module/branches'
package_list_url = root_url + 'module/packages'

env_list_url = root_url + 'envs'

job_url = root_url + 'job/run'


hint = 'Press Enter to select'


def gen_wf():
    return Workflow3(help_url='https://github.com/Thare-Lam/alfred-zcy-jenkins',
                     update_settings={
                         'github_slug': 'Thare-Lam/alfred-zcy-jenkins',
                         'frequency': 1
                     })
