from setuptools import setup, find_packages

setup(
    name='arclib',
    packages=['arclib'],
    version='1.0.0',
    description='一个用于处理Arcaea谱面 (*.aff) 相关的Python包',
    author='lam0578',
    author_email='1805096805@qq.com',
    url='https://github.com/LAM0578/Python-Arcaea-Library',
    download_url='https://github.com/LAM0578/Python-Arcaea-Library/archive/main.zip',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'
    ]
)
