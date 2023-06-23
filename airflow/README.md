# Instructions

## Setup Project

```sh
git clone git@github.com:BuggedCat/airflow-scrapy-poc.git 
```

## Airflow local

```sh
cd airflow
python -m venv .venv
source ./.venv/bin/activate
export AIRFLOW_HOME="$(pwd)"
```

### Install Python dependencies

`pip install -r requirements.txt`

To use Airflow Docker Operator

`pip install apache-airflow-providers-docker`

### Configure Airflow

**Important: Before running airflow commands run this command in the airflow directory**

`export AIRFLOW_HOME="$(pwd)"`

#### Configure airflow directory and databases

In the `airflow.cfg` file, modify the value of the `sql_alchemy_conn` parameter to an absolute path. Replace it with the appropriate path specific to your `airflow_home`. Here's an example:

`sql_alchemy_conn=sqlite:////home/gian/projects/airflow-scrapy-poc/airflow/airflow.db`

Ensure that you replace `/home/gian/projects/airflow-scrapy-poc/airflow/airflow.db` with the correct absolute path for your `airflow_home`.

Run the following commands in the shell:

```
airflow db init
airflow db check
```

#### Create an airflow user

```
airflow users create --username admin \
    --password admin \
    --firstname Bugged \
    --lastname Cat \
    --role Admin \
    --email test.main@mail.com
```

#### Running Airflow

Open two terminal windows/tabs go to your airflow home path and run:

```sh
# Start Webserver on terminal 1
export AIRFLOW_HOME="$(pwd)"
airflow webserver
```

```sh
# Start Webserver on terminal 2
export AIRFLOW_HOME="$(pwd)"
airflow scheduler
```

Go to http://localhost:8080, the `user` and `password` is `admin` and `admin`, you should see the airflow home.

![Airflow Web Home](/docs/imgs/airflow_start_page.png "Airflow Web Home")


#### The DAG

In the `dags` folder there is a python file `sample_spider.py`

Replace both this lines with the path to the `crawler` project that is in this repo, or the path where you want the data and logs to be stored.

```python
docker_task = DockerOperator(
    ...
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
```

The `source` parameter is the location from which you will mount the `target` path inside the container. In the case of the crawler container, it stores the logs and data internally at `/code/{logs, data}`, which is why it is pointing to those paths instead of the actual path of the `crawler` project. If you want to change this behavior, you can modify the Dockerfile and the Spider python file in the `crawler` project.

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

### Running the DAG

Before running the DAG building the dockerfile project is needed