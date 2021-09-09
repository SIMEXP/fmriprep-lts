# inspired from https://github.com/xolox/python-humanfriendly/blob/master/Makefile

PACKAGE_NAME = $(shell python3 setup.py --name)
PACKAGE_VERSION = $(shell python3 setup.py --version)

default:
	@echo "Makefile for $(PACKAGE_NAME) $(PACKAGE_VERSION)"
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make install    build the package'
	@echo '    make test       run the test suite'
	@echo '    make reports    build the jupyter reports'
	@echo '    make publish    publish changes to GitHub/PyPI'
	@echo '    make clean      cleanup all temporary files'
	@echo

install:
	@$(MAKE) clean
	@python3 -m pip install -r requirements.txt
# @python3 setup.py sdist bdist_wheel
# @python3 -m pip install -e .

test: 
	@pytest code/tests/

reports:
# jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute --to html $HOME/Documents/work/fmriprep-lts/code/visualization/report.ipynb --output $HOME/Documents/work/fmriprep-lts/outputs/ieee/stability_report_ds000256/report_multiprocess.html

publish:
# @git push origin && git push --tags origin
# @python3 -m pip install twine wheel setuptools
# @$(MAKE) install
# @python3 -m twine upload dist/*
# @$(MAKE) clean

publish-test:
# push tests on another datalad repo ?

clean:
	@rm -Rf *.egg *.egg-info .cache .coverage .tox build dist docs/build htmlcov
	@find -depth -type d -name __pycache__ -exec rm -Rf {} \;
	@find -type f -name '*.pyc' -delete
