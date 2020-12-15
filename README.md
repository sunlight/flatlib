# riftlib

Riftlib is a fork of [Flatangle's Flatlib](https://github.com/flatangle/flatlib) python library for Traditional Astrology. Much gratitude goes to João Ventura for laying the difficult groundwork from which I've built.

```python
>>> date = Datetime('2015-03-13', '17:00', '+00:00')
>>> pos = GeoPos('38n32', '8w54')
>>> chart = Chart(date, pos)

>>> sun = chart.get(const.SUN)
>>> print(sun)
<Sun Pisces +22:47:25 +00:59:51>
```

## Documentation

Flatlib's original documentation is available at [http://flatlib.readthedocs.org/](http://flatlib.readthedocs.org/). Riftlib offers additional features which will appear in this readme.


## Installation

Riftlib is a Python 3 package, make sure you have Python 3 installed on your system.

You can install riftlib with `pip3 install riftlib` or download the latest stable version from [https://pypi.python.org/pypi/riftlib](https://pypi.python.org/pypi/riftlib) and install it with `python3 setup.py install`.


## Development

You can clone this repository or download a zip file using the right side buttons.