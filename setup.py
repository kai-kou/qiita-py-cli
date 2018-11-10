from setuptools import setup, find_packages


setup(
  name="qiita-py-cli",
  version="0.0.2",
  description="Qiita API v2のコマンドラインツール",
  author="kai_kou",
  packages=find_packages(),
  install_requires=['docopt'],
  dependency_links=['git+ssh://git@github.com/kai-kou/qiita_py#egg=python_dateutil'],
  entry_points={
    "console_scripts": [
      "qiita=qiita.core:main",
    ]
  },
  classifiers=[
    'Programming Language :: Python :: 3.6',
  ]
)