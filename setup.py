from setuptools import setup
import fastentrypoints

setup(
    name='lazydots',
    version='0.0',
    author='Aaron Christianson',
    license='BSD',
    author_email='ninjaaron@gmail.com',
    url='https://github.com/ninjaaron/wrld',
    description='make pointed hebrew from ascii characters',
    long_description=open('README.rst').read(),
    keywords='hebrew',
    py_modules=['lazydots'],
    entry_points={'console_scripts': ['lzd=lazydots:main']},
    install_requires=['deromanize', 'PyYaml'],
)
