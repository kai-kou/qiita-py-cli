from docopt import docopt

from qiita_v2.client import QiitaClient

import os

from os.path import expanduser

import re

import json


def main():
  _USAGE = '''
  Qiita Python CLI

  Usage:
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
  print(f'command: {command[0]}')
  print(f'options: {options}')
  params.extend(options)

  home = expanduser("~")
  config_file = os.path.join(home, '.qiita-cli.yaml')
  client = QiitaClient(config_file=config_file)
  res = getattr(client, command[0])(*params)
  print(res.to_json())


if __name__ == '__main__':
  main()