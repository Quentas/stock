## Start

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages:

```bash
pip install -r requirements.txt
```
After that run Redis server:
```bash
redis-server
```
or with [redis-windows](https://github.com/zkteco-home/redis-windows)

## Usage
To fill database with entries run 

```bash
python manage.py generate_product <amount_of_categories> <amount_of_products>
```
To set random values for Product ```price```, ```status``` and ```remains``` run
```bash
python manage.py setvals
```