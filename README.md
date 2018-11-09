# qiita-py-cli

## Usage

Qiitaにログインしてアクセストークンを取得して環境変数に設定してください。  
スコープは```read``` と```write``` を指定する必要があります。  

https://qiita.com/api/v2/access_tokens


### GitHubから取得

```sh
> git clone https://github.com/kai-kou/qiita-py-cli.git
> cd qiita-py-cli
> python setup.py install

# bash
> export QIITA_PY_CLI_ACCESS_TOKEN=<Qiitaのアクセストークン>

# fish
> set -x QIITA_PY_CLI_ACCESS_TOKEN <Qiitaのアクセストークン>

> qiita get_user kai_kou
```
