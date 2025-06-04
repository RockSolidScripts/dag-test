from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow"
}

with DAG(
    dag_id="spark_pi_via_spark_operator",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["spark", "kubernetes"]
) as dag:

    submit_spark_pi = SparkKubernetesOperator(
        task_id="submit_spark_pi",
        namespace="spark-test",
        application_file="spark_pi.yaml",  # adjust path if different
        kubernetes_conn_id="kubernetes_default",
        do_xcom_push=False
    )
