from setuptools import setup, find_packages

description = """
Extract installed modules from an odoo server and 
build a meta package that will install those modules.
"""

requires = [
    'psycopg2',
]

setup(name='MetaOdoo',
      install_requires=requires,
      description=description,
      version="0.1",
      license="GPL",
      packages=find_packages(),
      zip_safe=True,
      entry_points={'console_scripts': ['metaodoo = metaodoo:main']})
