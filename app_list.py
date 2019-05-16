import sys
import json
from workflow import ICON_SYNC, web
from base import gen_wf, app_list_url, hint

CACHE_KEY_APP_LIST = 'zcy-jenkins-app-list-v20190507'
CACHE_TIMEOUT_APP_LIST = 24 * 60 * 60

EMPTY_APP = 'Empty app list'


def main(wf):
    keyword = wf.args[0] if len(wf.args) > 0 else None
    result = wf.cached_data(CACHE_KEY_APP_LIST, get_app_list, CACHE_TIMEOUT_APP_LIST)
    if result.get('errcode') != 0:
        clear_cache(wf)
        wf.add_item(title=result.get('errmsg'))
    else:
        app_list = result.get('result')
        if not isinstance(app_list, list) or len(app_list) == 0:
            # clear cache
            clear_cache(wf)
            wf.add_item(title=EMPTY_APP)
        else:
            app_list = filter(lambda x: keyword in x, result.get('result'))
            for app in app_list:
                wf.add_item(title=app, subtitle=hint, arg=app, valid=True)
    wf.send_feedback()


def clear_cache(wf):
    wf.cache_data(CACHE_KEY_APP_LIST, None)


def get_app_list():
    resp = web.get(app_list_url)
    resp.raise_for_status()
    return json.loads(resp.content)


def run():
    wf = gen_wf()
    if wf.update_available:
        wf.add_item('New version available', 'Action this item to install the update',
                    autocomplete='workflow:update', icon=ICON_SYNC)
    sys.exit(wf.run(main))