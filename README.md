# The Tensox Extract Transform Load

[![Try it on gitpod](https://img.shields.io/badge/try-on%20gitpod-brightgreen.svg)](https://gitpod.io/#https://github.com/The-Tensox/the-tensox-etl)
[![Build Status](https://img.shields.io/circleci/project/The-Tensox/the-tensox-etl/master.svg)](https://circleci.com/gh/The-Tensox/the-tensox-etl)

Will either ingest synthetic data into the data warehouse, either gather world data from multiple sources (Google Earth, datasets, APIs ...) into it.

Later we could think also of generating "synthetic data" from real world data using deep learning (probably via other components).

## Installation

```bash
python3 -m virtualenv env
source env/bin/activate
pip install -R requirements.txt
```

## Usage

```bash
wget -O heightmap.png https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73934/gebco_08_rev_elev_21600x10800.png
```

```python
python main.py
```