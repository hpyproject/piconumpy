
ifeq ($(PYTHON),)
PYTHON := python3
endif

IMPLEMENTATION := $(shell $(PYTHON) -c "import sys; print(sys.implementation.name)")


all:
	make editable_universal
ifeq ($(IMPLEMENTATION),cpython)
	make editable
endif


rm_hpy_py:
	rm -f piconumpy/_piconumpy_hpy.py

editable:
	$(PYTHON) -m pip install -e .
	make rm_hpy_py

editable_universal:
	$(PYTHON) -m pip install -e . --config-settings="--global-option=--hpy-abi=universal"
	make rm_hpy_py

editable_full:
	$(PYTHON) -m pip install -e .[full]
	make rm_hpy_py


# deprecated but let's keep them
develop:
	$(PYTHON) setup.py develop
	make rm_hpy_py

develop_universal:
	$(PYTHON) setup.py --hpy-abi=universal develop
	make rm_hpy_py

build_ext_universal:
	$(PYTHON) setup.py --hpy-abi=universal build_ext -if
	make rm_hpy_py

build_ext:
	$(PYTHON) setup.py build_ext -if
	make rm_hpy_py


format:
	black -l 82 setup.py piconumpy/*.py
	clang-format-7 -i piconumpy/*cpython_capi.c

tests: rm_hpy_py
	$(PYTHON) -m pytest piconumpy -s

clean:
	rm -f piconumpy/*.so
	rm -rf build dist piconumpy.egg-info

black:
	black -l 82 .


install_pypy:
	uv python install pypy

install_graalpy:
	uv python install graalpy

create_venv_cpy:
	$(PYTHON) -m venv .venv_cpy --upgrade-deps

create_venv_pypy:
	$(shell uv python find pypy) -m venv .venv_pypy --upgrade-deps

create_venv_graalpy:
	# cannot use --upgrade-deps because pip is patched for GraalPy
	$(shell uv python find graalpy) -m venv .venv_graalpy
