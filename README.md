Pybab: python interface to geotree

Installation:
- Install geotree_core, geotree_api_core and geotree_django in a postgresql database with postgis.
  Postgres must be at least version 9.2 and postgis must be at least version 2.0

- Install the package in python:
```bash
python setup.py install
```

- Add the following to your installed apps.
```python
INSTALLED_APPS += ('pyhive.extra.django', 'pybab', 'pybab.api')
```
and this to your template loaders:
```python
TEMPLATE_LOADERS += ('django.template.loaders.eggs.Loader',)
```

- Tweack the settings
- Enjoy
