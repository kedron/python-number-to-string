#!/bin/bash
#
USAGE="build_python_module.sh <module_directory>"
#

if [[ $# != 1 || ! -d "$1" ]]
then
    echo $USAGE
    exit -1
fi

MODULE_DIR="$1"
MODULE_NAME=$(basename $MODULE_DIR)
cd $MODULE_DIR

# Find all .po files to be compiled to .mo message catalogs
for i in $(find . -name "*.po")
do
    pofile=$i
    directory=$(dirname $i)
    basename=$(basename $i)
    localename=${basename%.po}
    mkdir -p $MODULE_NAME/share/$localename/LC_MESSAGES
    python setup.py compile_catalog --input-file $i --locale $localename --domain $MODULE_NAME --directory $MODULE_NAME/share
done

python setup.py build
