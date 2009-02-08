from setuptools import setup, find_packages
 
version = '0.1'
 
LONG_DESCRIPTION = """
The django-wall app allows for shared posting and display of short
text items in a communal setting. The app is designed to be reusable
and extensible and was built with Pinax deployment in mind.
"""
 
setup(
    name='django-wall',
    version=version,
    description="django-wall",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Other/Nonlisted Topic",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='wall,pinax,django',
    author='Rock Howard',
    author_email='rockmhoward@gmail.com',
    url='http://django-wall.googlecode.com/',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
