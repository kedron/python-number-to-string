python-number-to-string
=======================

python-number-to-string is a project that implements the translation of an integer
number into its corresponding natural language translation.  It attempts to be as 
language-agnostic as possible, allowing for translations to several languages.

Basic Algorithm
---------------

The difficulty of the task of natural language translation of numbers is that the
translation is only semi-regularized.  There are some patterns we can deduce and
write and algorithm code for, such as the tendency of most languages to group large 
numbers by every 3 decimal orders of magnitude (although as we'll see there are 
some exceptions).  Other aspects of the translation are not regular at all and 
are different for every language.  Thus, one must find a way to model the unique
aspects of each language in a data structure while encapsulating the common patterns 
into code.

I have chosen to store the unique parts of each language into a set of hash tables
which I then query during translation.  The data for each language includes names
of numbers, characters used to separate numerical values, punctuation, and a few
special cases.  Some of this data is similar to that available in a traditional
locale database.  Unfortunately, locale databases do not contain the complete and 
exact data I need, so I could not simply use what already exists.

Instead, I am using a portion of the locale model, LC\_MESSAGES, to implement my 
database.  For each locale, I build a dictionary of values which are transformed
using python's gettext module.  Thus, all I need to do to add a language is to copy 
my locale source file, and translate each necessary string.  The locale sources
are automatically compiled into python-readable .mo files during the build process
and made available to my program.

Given a locale hash, I then only need to implement a few simple tasks for translating
a number:

    1. Write a function that translates a number between 1 and 999.  This is done
       using the hash table along with a few regularized rules.
    2. Iterate over every 3 orders of magnitude (base 10), building a string as
       we go.
    3. Add any opening/closing flourishes, as necessary.

To find out more, check out the algorithm at lib/NumberToString/NumberToString/NumberToString.py

LIMITATIONS
-----------
The project suffers from the following limitations:

    * Only works for languages that count using groupings of thousands.  Languages
      such as Hindi which group using lakhs (100,000) and crores (10,000,000) are 
      not currently supported.
    * I've arbitrarily set a number limit of 1,000 decillion -1, just to minimize the
      amount of translation necessary.
    * Currently, project has only been tested in my local environment (OS X Mavericks,
      CentOS 7 running on a Virtual Box VM under Vagrant 1.6.3, python 2.7).
    * Currently, project has only been tested on languages using latin-derived characters 
      (although utf-8 is the charset used).

Future Improvements
-------------------

    * deployment scripts to staging and production environments
    * server-side git hook to run style-check and test suite on every checkout
    * Add support for Ubuntu 12/14 and Debian 6/7
    * Add support for python 3
    * verify functionality for non-latin languages and charsets
    * Add support for (mostly South-Asian) languages not using a thousands grouping
    * Install locale message files to system path rather than python module path

Project Components
------------------
The project consists of the following resources (ordered by repo structure):

    /repo - top directory of the repo
        - /app - end-user applications that use the underlying implementation to provide
                 translation services.
            - cmd/ - command-line script to translate numbers to text    
            - flask/ - REST API for translating numbers to text
            - html/ - simple ajax form for using REST API
            - run_unit_tests/ - runs unit tests (duh!)
        - deploy/ - code and configurations for deploying code to various environments
            - vagrant/ - code to auto-deploy a working local test environment using virtualbox VMs
        - lib/ - underlying algorithmic implementations used by applications
            - NumberToString/ - python module implementing number-to-string algorithm 
                - NumberToString.py - code implementing the base algorithm
                - NumberToString/i18n/ - message catalogs implementing different languages
                - tests/ - unit tests for NumberToString module
        - package/ - build scripts for building and packaging artifacts

Instructions for creating a development environment
---------------------------------------------------

1. Acquire an OS X system running Mavericks or Mountain Lion.

2. Install the latest version of Virtual Box from https://www.virtualbox.org/wiki/Downloads

3. Install the latest Vagrant from http://www.vagrantup.com/downloads.html

4. clone this repo, e.g. 'git clone git@github.com:kedron/python-number-to-string.git'

5. Deploy the Virtual Box VM. See python-number-to-string/deploy/vagrant/Vagrantfile for any
   config variables you may want to change.

         $ cd python-number-to-string/deploy/vagrant
         $ vagrant box add vagrant box add developervms/centos7-64
         (go take a coffee break)
         $ vagrant up
         (go take another coffee break)  
         (and check your email)
         (When you get back, there will be some warnings from puppet you can safely ignore)
         $ vagrant ssh
         $ sudo su -
         # cd python-number-to-string

6. Vagrant has deployed a CentOS 7 vm with all of the dependencies you need to develop and
   test.  It has also mounted the top-level repo directory in /root/python-number-to-string
   This allows you to work with files using your preferred tools in the OS X environment, while
   any changes made are seen inside the VM.  
   
7. Next, let's build and install the NumberToString python module.  

         # cd package
         # ./build_python_module.sh /root/python-number-to-string-dev/lib/NumberToString
         Congratulations! Your package has been built to /tmp/tmp.dijDXpVEwK/dist/NumberToString-0.0.1.tar.gz

   This script will build and package all code and related-resources needed and create an 
   installable module in the lib/NumberToString/dist sub-directory.  This module can then 
   be installed using pip or another module installer: 

         # pip install /tmp/tmp.dijDXpVEwK/dist/NumberToString-0.0.1.linux-x86\_64.tar.gz

8. Now, we can use the command-line application:

         # cd /root/python-number-to-string-dev/app/cmd
         # python number-to-string.py 123
         one hundred and twenty-three.
         # python number-to-string.py 123 --locale=en_CA
         one hundred and twenty-three, eh?

9. We can also run the test suite:

         # cd /root/python-number-to-string-dev/app/run_unit_tests
         # python run-unit-tests.py --locale=all
         Running Test Suite for en_US...
         .
         ----------------------------------------------------------------------
         Ran 1 test in 0.025s
         
         OK
         Running Test Suite for en_GB...
         .
         ----------------------------------------------------------------------
         Ran 1 test in 0.010s
         
         OK
         Running Test Suite for en_CA...
         .
         ----------------------------------------------------------------------
         Ran 1 test in 0.011s
         
         OK
