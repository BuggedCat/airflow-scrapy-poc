# Instructions

## Setup Project

```sh
mkdir -p airflow-scrapy/airflow
mkdir -p airflow-scrapy/crawler
```

## Airflow local

```sh
cd airflow-scrapy/airflow
python -m venv .venv
source ./.venv/bin/activate
export AIRFLOW_HOME="$(pwd)"
mkdir dags
```

### Install script

```sh
AIRFLOW_VERSION=2.6.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-no-providers-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### Configure Airflow

To use Docker Operator

`pip install apache-airflow-providers-docker`

### Important: **Before running airflow commands run in the airflow root directory**

`export AIRFLOW_HOME="$(pwd)"`

#### Configure airflow directory and databases

```
airflow db init
airflow db check
```

On the airflow.cfg file change this line from True to False

`load_examples = False`

#### Create user
```
airflow users create --username admin \
    --password admin \
    --firstname Bugged \
    --lastname Cat \
    --role Admin \
    --email test.main@mail.com
```

#### Running Airflow

Open two terminal windows and run:

```sh
# Start Webserver on terminal 1
cd <your airflow home path>
export AIRFLOW_HOME="$(pwd)"
airflow webserver
```

```sh
# Start Webserver on terminal 2
cd <your airflow home path>
export AIRFLOW_HOME="$(pwd)"
airflow scheduler
```

Go to http://localhost:8080, the `user` and `password` is `admin` and `admin`.
