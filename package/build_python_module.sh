#!/bin/bash
#
USAGE="build_python_module.sh <module_directory>"
#
# 1. Copy source module directory to /tmp/<tempname>
# 2. Compile all message catalogs
# 3. Run the sdist command to build a package

if [[ $# != 1 || ! -d "$1" ]]
then
    echo $USAGE
    exit -1
fi

MODULE_DIR="$1"
if [[ "$MODULE_DIR" == "." ]]
then
    MODULE_NAME=$(basename $(readlink -f $MODULE_DIR))
else
    MODULE_NAME=$(basename $MODULE_DIR)
fi

# 1. Copy source module directory to /tmp/<tempname>
#    Since virtual box does not support link creation in shared directories,
#    we have to copy the module directory to /tmp before unleashing setuptools
#    on it.
WORK_DIR=$(mktemp -d)
cd $WORK_DIR
LOG_FILE=$(mktemp --tmpdir=.)
echo "rsync -av $MODULE_DIR $WORK_DIR" >> $LOG_FILE 2>&1
rsync -av $MODULE_DIR $WORK_DIR >> $LOG_FILE 2>&1
echo "cd $WORK_DIR" >> $LOG_FILE 2>&1

# 2. Compile all message catalogs - Find all .po files in the module source
#    tree, use setuptools/babel integration to compile them to .mo catalogs
for i in $(find . -name "*.po")
do
    pofile=$i
    directory=$(dirname $i)
    basename=$(basename $i)
    localename=${basename%.po}
    echo "+mkdir -p $MODULE_NAME/share/$localename/LC_MESSAGES" >> $LOG_FILE 2>&1
    mkdir -p $MODULE_NAME/share/$localename/LC_MESSAGES >> $LOG_FILE 2>&1
    if [[ $? != 0 ]]
    then
        echo "An Error occurred: mkdir -p command failed"
        cat $LOG_FILE
        exit -1
    fi
    echo "+python setup.py compile_catalog --input-file $i --locale $localename --domain $MODULE_NAME --directory $MODULE_NAME/share" >> $LOG_FILE 2>&1 
    python setup.py compile_catalog --input-file $i --locale $localename --domain $MODULE_NAME --directory $MODULE_NAME/share >> $LOG_FILE 2>&1
    if [[ $? != 0 ]]
    then
        echo "An Error occurred: compile_catalog command failed"
        cat $LOG_FILE
        exit -1
    fi
done

# 3. Run the sdist command to build a package
echo "python setup.py sdist" >> $LOG_FILE 2>&1
python setup.py -v sdist >> $LOG_FILE 2>&1
if [[ $? != 0 ]]
then
    echo "Alas! An Error occurred: sdist command failed"
    cat $LOG_FILE
    exit -1
fi

package=$(echo $WORK_DIR/dist/*.gz)
if [[ -f "$package" ]]
then
    echo "Congratulations! Your package has been built to $package"
else
    echo "Alas! An Error occurred: $package was not created."
    cat $LOG_FILE
    exit -1
fi
