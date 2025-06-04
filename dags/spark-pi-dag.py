from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.utils.dates import days_ago

spark_application_spec = {
    "apiVersion": "sparkoperator.k8s.io/v1beta2",
    "kind": "SparkApplication",
    "metadata": {
        "name": "spark-pi-python",
        "namespace": "spark-test"
    },
    "spec": {
        "type": "Python",
        "pythonVersion": "3",
        "mode": "cluster",
        "image": "05068384/spark-test:1.0",
        "imagePullPolicy": "IfNotPresent",
        "mainApplicationFile": "local:///app/app.py",
        "sparkVersion": "3.5.5",
        "driver": {
            "cores": 1,
            "memory": "512m",
            "serviceAccount": "spark-operator-spark",
            "securityContext": {
                "capabilities": {"drop": ["ALL"]},
                "runAsGroup": 185,
                "runAsUser": 185,
                "runAsNonRoot": True,
                "allowPrivilegeEscalation": False,
                "seccompProfile": {"type": "RuntimeDefault"}
            }
        },
        "executor": {
            "instances": 1,
            "cores": 1,
            "memory": "512m",
            "securityContext": {
                "capabilities": {"drop": ["ALL"]},
                "runAsGroup": 185,
                "runAsUser": 185,
                "runAsNonRoot": True,
                "allowPrivilegeEscalation": False,
                "seccompProfile": {"type": "RuntimeDefault"}
            }
        }
    }
}

default_args = {
    "owner": "airflow"
}

# TODO: Update the "SparkKubernetesOperator" args. 

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
        application=spark_application_spec,
        kubernetes_conn_id="kubernetes_default",  # default K8s connection
        do_xcom_push=False
    )
