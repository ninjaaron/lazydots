from setuptools import setup
import fastentrypoints

setup(
    name='lazydots',
    version='0.0',
    author='Aaron Christianson',
    license='MPL 2.0',
    author_email='ninjaaron@gmail.com',
    url='https://github.com/ninjaaron/lazydots',
    description='make pointed Hebrew from ascii characters',
    long_description=open('README.rst').read(),
    keywords='hebrew',
    packages=['lazydots'],
    entry_points={'console_scripts': ['lzd=lazydots:read_text']},
    install_requires=['deromanize', 'PyYaml'],
    include_package_data=True
)
