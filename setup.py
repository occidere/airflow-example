from setuptools import setup, find_packages
setup(
        name='airflow-example',
        version='1.0',
        author='occidere',
        author_email='occidere@naver.com',
        url='https://github.com/occidere/airflow-example',
        description='No Description',
        license='Apache 2.0',
        install_requires=[
            'apache-airflow',
            'requests',
            'selenium',
            'line-bot-sdk',
            'pyyaml',
            'setuptools',
            'wheel',
            'elasticsearch-curator',
            'elasticsearch',
        ],
        packages=find_packages(exclude=['venv', 'doc', 'test']),
        python_requires='>=3.5',
        package_data={
            'resources': ['resources/*']
        },
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ]
)

