from setuptools import setup

setup(
    app=["Emma.py"],
    setup_requires=["py2app"],
    data_files=[],
    options={
        'py2app': {
            'argv_emulation': True,
            'plist': {
                'LSUIElement': True,
            },
            'packages': [
                'appdirs',
                'django',
                'emma',
                'gunicorn',
                'pandas',
                'pillow',
                'plotly',
                'rumps',
            ],
        },
    },
)
