# qiita-py-cli

Qiita APIが簡単に利用できるCLIコマンドラインツールです。  

※Qiita:Teamには非対応。  

## Usage

Qiitaにログインしてアクセストークンを取得して環境変数に設定してください。  
スコープは```read``` と```write``` を指定する必要があります。  

https://qiita.com/api/v2/access_tokens


### GitHubから取得

```sh
> git clone https://github.com/kai-kou/qiita-py-cli.git
> cd qiita-py-cli
> python setup.py install

> qiita init
> qiita get_user kai_kou
```

Qiitaのアクセストークンは環境変数に設定することもできます。  

```sh
# bash
> export QIITA_PY_CLI_ACCESS_TOKEN=<Qiitaのアクセストークン>

# fish
> set -x QIITA_PY_CLI_ACCESS_TOKEN <Qiitaのアクセストークン>
```