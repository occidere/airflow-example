from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'occidere',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 14),
    'email': ['occidere@naver.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'queue': 'bash_queue',
    'pool': 'backfill',
    'priority_weight': '10',
    'end_date': datetime(2020, 1, 31)
}

dag = DAG('tutorial', default_args=default_args, schedule_interval=timedelta(minutes=1))

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag
)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag
)

# Jinja Template
templated_command = """
  {% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.company }}"
  {% endfor %} 
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'company': 'NAVER Corp'},
    dag=dag
)

# t2 will run if t1 ran successfully (Chain operation)
t2.set_upstream(t1)
# t1 >> t2
# t2 << t1

# Multiple chaining
t1 >> t2 >> t3
# t1.set_downstream([t2, t3])
# t1 >> [t2, t3]
# [t2, t3] << t1
