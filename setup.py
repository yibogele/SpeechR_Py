# import ez_setup
# ez_setup.use_setuptools()
# 这两行是当setuptools不存在时,自动从网上下载安装所需的setuptools包.

from setuptools import setup, find_packages
setup(
    name="SpeechRecognition",
    version="0.1",
    # package_dir={'': 'speech'},
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.conf', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    }
)

