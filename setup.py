from setuptools import setup

APP = ['koostos.py'] # your main scipt name
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None, # you can ass a .icons icon later
    'packages': ['ttkbootstrap', 'watchdog', 're'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)