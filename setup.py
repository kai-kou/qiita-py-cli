from setuptools import setup, find_packages


setup(
  name="QiitaPyCli",
  version="0.0.1",
  description="Qiita API v2のコマンドラインツール",
  author="kai_kou",
  packages=find_packages(),
  install_requires=['docopt'],
  dependency_links=['git+github.com/kai-kou/qiita_py'],
  entry_points={
    "console_scripts": [
      "qiita=qiita.core:main",
    ]
  },
  classifiers=[
    'Programming Language :: Python :: 3.6',
  ]
)