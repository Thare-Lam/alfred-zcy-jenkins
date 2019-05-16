import json
from workflow import web
from base import env_list_url

CACHE_KEY_ENV_LIST = 'env-list-v20190505'
CACHE_TIMEOUT_ENV_LIST = 7 * 24 * 60 * 60

EMPTY_ENV = 'Empty environment list'


def run(wf, keyword, add_item):
    result = wf.cached_data(CACHE_KEY_ENV_LIST, get_env_list, CACHE_TIMEOUT_ENV_LIST)
    if result.get('errcode') != 0:
        clear_cache(wf)
        wf.add_item(title=result.get('errmsg'))
    else:
        env_list = result.get('result')
        if not isinstance(env_list, list) or len(env_list) == 0:
            # clear cache
            clear_cache(wf)
            wf.add_item(title=EMPTY_ENV)
        else:
            env_list = filter(lambda x: keyword in x, result.get('result'))
            for env in env_list:
                add_item(env)
    wf.send_feedback()


def clear_cache(wf):
    wf.cache_data(CACHE_TIMEOUT_ENV_LIST, None)


def get_env_list():
    resp = web.get(env_list_url, params={
        'type': 'all'
    })
    resp.raise_for_status()
    return json.loads(resp.content)