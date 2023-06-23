# Instructions

## Setup Project

```sh
mkdir -p airflow-scrapy/airflow
mkdir -p airflow-scrapy/crawler
```

## Airflow local

```sh
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

On the `airflow.cfg` file change this line from True to False

`load_examples = False`

And change this line to your `airflow.db` path

`sql_alchemy_conn = sqlite:////home/user/your/airflow_home/path/airflow.db`

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
cd <your AIRFLOW_HOME path>
export AIRFLOW_HOME="$(pwd)"
airflow webserver
```

```sh
# Start Webserver on terminal 2
cd <your AIRFLOW_HOME path>
export AIRFLOW_HOME="$(pwd)"
airflow scheduler
```

Go to http://localhost:8080, the `user` and `password` is `admin` and `admin`.

#### Creating the DAG

In the dags folder create a python file `sample_spider.py`

- Replace the placeholder `your_project_path` with the path for the `crawler` project.

```python
from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    "start_date": datetime(2023, 1, 1),
    "depends_on_past": False,
}

SPIDER_NAME = "sample_spider"

with DAG(
    "scrapy_docker",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    docker_task = DockerOperator(
        task_id="run_my_docker_container",
        image="crawler-scrapy-airlfow",
        api_version="auto",
        auto_remove="never",
        command=f"scrapy crawl {SPIDER_NAME}",
        dag=dag,
        docker_url="unix://var/run/docker.sock",
        environment={"LOG_LEVEL": "INFO"},
        mounts=[
            Mount(
                source="<your_project_path>/crawler/data",
                target="/code/data",
                type="bind",
            ),
            Mount(
                source="<your_project_path>/crawler/logs",
                target="/code/logs",
                type="bind",
            ),
        ],
    )

    docker_task
```