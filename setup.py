from setuptools import setup, find_packages
import ella_category_subdomain

setup(
    name = 'Ella-Category-Subdomain',
    version = ella_category_subdomain.__versionstr__,
    description = 'Use Ella categories as subdomains.',
    long_description = 'Use selected Ella categories as subdomains without creating many sites.',
    author = 'Vitek Pliska',
    author_email='whit@jizak.cz',
    license = 'BSD',
    url='http://github.com/whit/',

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'tests')
    ),

    include_package_data = True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
        'setuptools>=0.6b1',
        'ella>=2.0',
    ],
)

