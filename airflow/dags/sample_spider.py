from datetime import datetime

from docker.types import Mount

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

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
                source="/home/gian/projects/airflow-scrapy-poc/crawler/data",
                target="/code/data",
                type="bind",
            ),
            Mount(
                source="/home/gian/projects/airflow-scrapy-poc/crawler/logs",
                target="/code/logs",
                type="bind",
            ),
        ],
    )

    docker_task  # type: ignore
