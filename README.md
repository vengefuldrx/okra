# okra - a fork of pyKwalify

# Usage

Create a data file. Json and yaml formats are both supported.

```yaml
- foo
- bar
```

Create a schema file with validation rules.

```yaml
type: seq
sequence:
  - type: str
```

Run validation from cli.

```bash
okra --data-file data.yaml --schema-file schema.yaml
```

If validation passes then return code from the invocation will be 0. If errors was found then 1.

Run validation from code. Multiple schema files is possible to use when using partial schemas (See doc for details).

```python
from okra.core import Core
c = Core(source_file="data.yaml", schema_files=["schema.yaml"])
c.validate(raise_exception=True)
```

If validation fails then exception will be raised.


## Runtime Dependencies

 - docopt 0.6.2
 - PyYaml 3.11


## Supported python version

 - Python 2.7
 - Python 3.2
 - Python 3.3
 - Python 3.4


# How to test

Install test requirements with

```
$ pip install -r dev-requirements.txt
```

Run tests with

```
$ py.test
```

or if you want to test against all python versions and pep8

```
$ tox
```


# Documentation

[Implemented validation rules](docs/Validation Rules.md)


# Licensing

MIT, See docs/License.txt for details

Copyright (c) 2013-2015 Johan Andersson
