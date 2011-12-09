from setuptools import setup
from ella_category_subdomain import __versionstr__

setup(
    name = 'Ella-Category-Subdomain',
    version = __versionstr__,
    description = 'Use Ella categories as subdomains.',
    long_description = """Use selected Ella categories as subdomains without
    the need to create many sites and for easier administration.

    It is usable for SEO, microsites, landing pages and similar things.""",
    author = 'Sanoma Media Praha s.r.o.',
    author_email = 'online-dev@sanomamedia.cz',
    maintainer = 'Vitek Pliska',
    maintainer_email='whit@jizak.cz',
    license = 'BSD',
    url='http://github.com/sanomacz/ella-category-subdomain/',

    packages = ('ella_category_subdomain',),
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

