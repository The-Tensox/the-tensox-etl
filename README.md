# The Tensox Extract Transform Load

Will either ingest synthetic data into the data warehouse, either gather world data from multiple sources (Google Earth, datasets, APIs ...) into it.

Later we could think also of generating "synthetic data" from real world data using deep learning (probably via other components).


# Usage

```
echo -e "DATABASE_URL=postgres://postgres:mypass@localhost/the-tensox
ROCKET_ADDRESS=localhost
ROCKET_PORT=8001" > .env
```
    cargo run