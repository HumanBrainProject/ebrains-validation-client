import os
from setuptools import setup

def package_files(base_dir, directory):
    pwd = os.getcwd()
    os.chdir(base_dir)
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    os.chdir(pwd)
    return paths

json_files = package_files('hbp_validation_framework', 'jsonTreeViewer')

setup(
    name='hbp_validation_framework',
    version='0.4.1',
    packages=['hbp_validation_framework'],
    package_data={'': json_files},
    url='https://github.com/HumanBrainProject/hbp-validation-client',
    license='BSD',
    author='Andrew Davison and Shailesh Appukuttan',
    author_email='andrew.davison@unic.cnrs-gif.fr, shailesh.appukuttan@unic.cnrs-gif.fr',
    description='Python client for the HBP Validation Framework web services',
    install_requires=['hbp-service-client', 'requests'],
    extras_require={'reports': ['fpdf', 'PyPDF2'],
                    'utils': ['sciunit']}
)
