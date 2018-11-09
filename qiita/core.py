from docopt import docopt

from qiita_v2.client import QiitaClient

import os

from os.path import expanduser

import re

import json

import yaml

from qiita.qiita_api_auth import QiitaAccessTokenHandler

from os.path import expanduser


def main():
    _USAGE = '''
  Qiita Python CLI

  Usage:
    qiita init
    qiita create_access_token [--params=<kn> --headers=<kn>]
    qiita create_expanded_template [--params=<kn> --headers=<kn>]
    qiita create_item [--params=<kn> --headers=<kn>]
    qiita create_item_comment <item_id> [--params=<kn> --headers=<kn>]
    qiita create_project [--params=<kn> --headers=<kn>]
    qiita create_template [--params=<kn> --headers=<kn>]
    qiita delete_access_token <token> [--params=<kn> --headers=<kn>]
    qiita delete_comment <id> [--params=<kn> --headers=<kn>]
    qiita delete_item <id> [--params=<kn> --headers=<kn>]
    qiita delete_project <id> [--params=<kn> --headers=<kn>]
    qiita delete_template <id> [--params=<kn> --headers=<kn>]
    qiita follow_tag <id> [--params=<kn> --headers=<kn>]
    qiita follow_user <user_id> [--params=<kn> --headers=<kn>]
    qiita get_authenticated_user [--params=<kn> --headers=<kn>]
    qiita get_authenticated_user_items [--params=<kn> --headers=<kn>]
    qiita get_comment <id> [--params=<kn> --headers=<kn>]
    qiita get_item <id> [--params=<kn> --headers=<kn>]
    qiita get_item_stock <item_id> [--params=<kn> --headers=<kn>]
    qiita get_project <id> [--params=<kn> --headers=<kn>]
    qiita get_tag <id> [--params=<kn> --headers=<kn>]
    qiita get_tag_following <id> [--params=<kn> --headers=<kn>]
    qiita get_template <id> [--params=<kn> --headers=<kn>]
    qiita get_user <id> [--params=<kn> --headers=<kn>]
    qiita get_user_following <user_id> [--params=<kn> --headers=<kn>]
    qiita lgtm_item <item_id> [--params=<kn> --headers=<kn>]
    qiita list_item_comments <item_id> [--params=<kn> --headers=<kn>]
    qiita list_item_stockers <item_id> [--params=<kn> --headers=<kn>]
    qiita list_items [--params=<kn> --headers=<kn>]
    qiita list_projects [--params=<kn> --headers=<kn>]
    qiita list_tag_items <id> [--params=<kn> --headers=<kn>]
    qiita list_tags [--params=<kn> --headers=<kn>]
    qiita list_teams [--params=<kn> --headers=<kn>]
    qiita list_templates [--params=<kn> --headers=<kn>]
    qiita list_user_followees <user_id> [--params=<kn> --headers=<kn>]
    qiita list_user_followers <user_id> [--params=<kn> --headers=<kn>]
    qiita list_user_following_tags <user_id> [--params=<kn> --headers=<kn>]
    qiita list_user_items <user_id> [--params=<kn> --headers=<kn>]
    qiita list_user_stocks <user_id> [--params=<kn> --headers=<kn>]
    qiita list_users [--params=<kn> --headers=<kn>]
    qiita stock_item <item_id> [--params=<kn> --headers=<kn>]
    qiita team [--params=<kn> --headers=<kn>]
    qiita thank_comment <comment_id> [--params=<kn> --headers=<kn>]
    qiita unfollow_tag <id> [--params=<kn> --headers=<kn>]
    qiita unfollow_user <user_id> [--params=<kn> --headers=<kn>]
    qiita unlgtm_item <item_id> [--params=<kn> --headers=<kn>]
    qiita unstock_item <item_id> [--params=<kn> --headers=<kn>]
    qiita unthank_comment <comment_id> [--params=<kn> --headers=<kn>]
    qiita update_comment <id> [--params=<kn> --headers=<kn>]
    qiita update_item <id> [--params=<kn> --headers=<kn>]
    qiita update_project <id> [--params=<kn> --headers=<kn>]
    qiita update_template <id> [--params=<kn> --headers=<kn>]

  Options:
    --help             ヘルプを表示
    --params=<kn>      params [default: None]
    --headers=<kn>     headers [default: None]
  '''
    all_params = docopt(_USAGE)
    command = [k for k, v in all_params.items() if v == True]
    params = [
        v for k, v in all_params.items()
        if re.match(r'\<.*\>', k) and v is not None]
    options = [
        json.loads(v) for k, v in all_params.items()
        if re.match(r'^\-', k) and v != 'None']
    params.extend(options)

    is_init = command[0] == 'init'
    access_token = get_access_token(is_init)

    if access_token is None and is_init == False:
      print('利用するにはQiitaのreadとwriteが許可されたアクセストークンが必要です')
      print('アクセストークンを取得するにはQiitaにログインして下記のURLへアクセスしてください')
      print('https://qiita.com/settings/tokens/new')
      return

    if is_init:
      return

    client = QiitaClient(access_token=access_token)
    res = getattr(client, command[0])(*params)
    print(json.dumps(res.to_json(), ensure_ascii=False))


def get_access_token(init=False):
  access_token_name = 'QIITA_PY_CLI_ACCESS_TOKEN'

  if init == False:
    # 環境変数から取得する
    access_token = os.getenv(access_token_name)
    if access_token is not None:
      return access_token

    # 設定ファイルから取得する
    config = get_config()
    if access_token_name in config:
      return config[access_token_name]

  # Oauth2認証で取得する
  client_id = os.getenv('QIITA_PY_CLI_CLIENT_ID')
  client_secret = os.getenv('QIITA_PY_CLI_CLIENT_SECRET')
  if client_id is not None and client_secret is not None:
    token_handler = QiitaAccessTokenHandler(client_id, client_secret)
    access_token = token_handler.get_access_token()
  else:
    access_token = input('Qiitaのアクセストークンを入力してください: ')

  if access_token != '':
    put_config({access_token_name: access_token})
  else:
    access_token = os.getenv(access_token_name)
  return access_token


def get_config():
  config = {}
  file_path = _get_config_path()
  if os.path.isfile(file_path):
    with open(file_path, 'r') as config_file:
      config = yaml.load(config_file)
  return config


def put_config(config):
  file_path = _get_config_path()
  with open(file_path, 'w') as config_file:
    yaml.dump(config, config_file, default_flow_style=False)


def _get_config_path():
  home = expanduser("~")
  return f'{home}/.qiita-py-cli.yml'

if __name__ == '__main__':
  main()
