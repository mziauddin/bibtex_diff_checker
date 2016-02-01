from setuptools import setup
#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.

setup(name='Bibtex_Difference_Checker',
      version='1.8',
      description='This application aims to compare two bibtliographical reference database (.bib) files and allow the user to keep the reference records in sync on both the files',
      # url='http://github.com/storborg/funniest',
      author='Mohammed Ziauddin',
      author_email='mdziauddin@ku.edu',
      # license='MIT',
      packages=['bibtex_diff_checker'],
      install_requires=[
          'bibtexparser','gitpython','Cython','unqlite==0.2.0'
      ],      
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['script'],
      classifiers = [
              'Programming Language :: Python',
              'Development Status :: 4 - Beta',
              'Natural Language :: English',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: Apache Software License',
              'Operating System :: OS Independent',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Software Development :: Libraries :: Application Frameworks',
              ],
      zip_safe=False)