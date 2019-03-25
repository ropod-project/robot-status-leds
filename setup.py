from setuptools import setup, find_packages

setup(name='status_leds',
      version='1.0.0',
      description='A library for displaying robot status through LEDs',
      url='https://github.com/ropod-project/robot-status-leds',
      author='Dharmin Bakaraniya',
      author_email='dharmin.bakaraniya@smail.inf.h-brs.de',
      keywords='component_monitoring robot_failures robot_status robotics',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      project_urls={
          'Source': 'https://github.com/ropod-project/robot-status-leds'
      })
