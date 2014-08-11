python-number-to-string
=======================
python-number-to-string is a project that implements the translation of an integer
number into its corresponding natural language translation.  It attempts to be as 
language-agnostic as possible, allowing for translations to several languages.

LIMITATIONS
-----------
The project suffers from the following limitations:
    * Only works for languages that count using groupings of thousands.  Languages
      such as Hindi which group using lakhs (100,000) and crores (10,000,000) are 
      not currently supported.
    * I've arbitrarily set a number limit of 1,000 decillion, just to minimize the
      amount of translation necessary.
    * Currently, project has only been tested in my local environment (OS X Mavericks,
      CentOS 6 running on a virtual box VM under Vagrant 1.6.3, python 2.6)

Future Improvements
-------------------
    * deployment scripts to staging and production environments

Project Components
------------------
The project consists of the following resources (ordered by repo structure):

/repo - top directory of the repo
    - /app - end-user applications that use the underlying implementation to provide
             translation services.
        - cmd/ - command-line script to translate numbers to text    
        - flask/ - REST API for translating numbers to text
        - html/ - simple ajax form for using REST API
    - deploy/ - code and configurations for deploying code to various environments
        - vagrant/ - code to auto-deploy a working local test environment using virtualbox VMs
    - lib/ - underlying algorithmic implementations used by applications
        - NumberToString/ - python module implementing number-to-string algorithm 
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
    $ vagrant up
    $ vagrant ssh
    $ sudo su -
    # cd python-number-to-string

6. Vagrant has deployed a CentOS 6 vm with all of the dependencies you need to develop and
   test.  It has also mounted the top-level repo directory in /root/python-number-to-string
   This allows you to work with files using your preferred tools in the OS X environment, while
   any changes made are seen inside the VM.  
7. Let's build the NumberToString python module.  

    # cd package
    # ./build_python_module.sh /root/python-number-to-string/lib/NumberToString

   The build script should have dumped 
