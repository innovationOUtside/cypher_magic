from setuptools import setup

setup(name='magic-cypher', 
      version='0.9.0', 
      description='',
      url='https://github.com/petehughes/cypher_magic',
      author='Pete Hughes',
      license='MIT',
      packages=['cypher-magic'],
      install_requires=['py2neo'],
      package_dir={'cypher-magic': 'cypher-magic'},
      package_data={'cypher-magic': ['assets/*.html']},
)