#!/bin/bash
type -P python > /dev/null && PYEXE=python || PYEXE=python3
if ! $PYEXE -c 'import sys; assert sys.version_info >= (3,10)' > /dev/null 2>&1; then
        echo "Found $($PYEXE -V)"
        echo "Expecting at least python 3.10 - exiting!"
        exit 1
fi

export PYTHONDONTWRITEBYTECODE=1

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ACDIR=$($PYEXE -c "import sys;print('Scripts' if sys.platform.startswith('win') else 'bin')")
$PYEXE -m venv --clear $MYPATH/.pytest
source $MYPATH/.pytest/$ACDIR/activate

ROSETTARUNTIMEDIR="../src/main/resources/runtime"
PYTHONCDMDIR="../target/python"
PYTHONUNITTESTDIR="../target/python_unit_tests"
echo "**** Install Dependencies ****"
$PYEXE -m pip install "pydantic>=2.6.1,<2.10"
$PYEXE -m pip install pytest
echo "**** Install Runtime ****"
$PYEXE -m pip install $MYPATH/$ROSETTARUNTIMEDIR/rosetta_runtime-2.1.0-py3-none-any.whl --force-reinstall
echo "**** Build and Install Generated Unit Tests ****"
cd $MYPATH/$PYTHONUNITTESTDIR
$PYEXE -m pip wheel --no-deps --only-binary :all: . || processError
$PYEXE -m pip install python_rosetta_dsl-0.0.0-py3-none-any.whl
cd $MYPATH
echo "**** Install CDM ****"

# run tests
$PYEXE -m pytest -p no:cacheprovider $MYPATH/runtime_tests $MYPATH/rosetta_tests 

rm -rf .pytest