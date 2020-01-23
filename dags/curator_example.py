from curator import *
from elasticsearch import *

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'occidere',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 23),
    'email': ['occidere@naver.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(dag_id='curator.example', default_args=default_args, schedule_interval='30 0 * * *') as dag:
    # pattern example: ^(test|feed)-\\d{6}$
    def _create_index_list(target_indices_pattern: str, days: int) -> IndexList:
        index_list = IndexList(client=Elasticsearch(hosts=['localhost:9200']))
        index_list.filter_by_regex(kind='regex', value=target_indices_pattern)
        index_list.filter_by_age(source='name', direction='older', timestring='%y%m%d', unit='days', unit_count=days)
        return index_list


    def delete_indices(target_indices_pattern: str, days: int) -> None:
        index_list = _create_index_list(target_indices_pattern, days)
        delete_index_list = DeleteIndices(index_list)
        try:
            delete_index_list.do_dry_run()
            # delete_index_list.do_action()
        except Exception as e:
            print(e)


    def refresh_off(target_indices_pattern: str, days: int) -> None:
        index_list = _create_index_list(target_indices_pattern, days)
        refresh_off_indices = IndexSettings(index_list, {'index': {'refresh_interval': '-1'}}, ignore_unavailable=True)
        try:
            refresh_off_indices.do_dry_run()
            # refresh_off_indices.do_action()
        except Exception as e:
            print(e)


    def to_warm(target_indices_pattern: str, days: int) -> None:
        index_list = _create_index_list(target_indices_pattern, days)
        to_warm_indices = Allocation(index_list, key='box_type', value='warm')
        try:
            to_warm_indices.do_dry_run()
            # to_warm_indices.do_action()
        except Exception as e:
            print(e)


    kickoff = DummyOperator(task_id='kickoff')

    t1_delete_indices = PythonOperator(
        task_id='delete_indices',
        python_callable=delete_indices,
        op_kwargs={'target_indices_pattern': '^(test|feed)-\\d{6}$', 'days': 7}
    )

    t2_refresh_off = PythonOperator(
        task_id='refresh_off',
        python_callable=refresh_off,
        op_kwargs={'target_indices_pattern': '^(test|feed)-\\d{6}$', 'days': 1}
    )

    t3_to_warm_indices = PythonOperator(
        task_id='to_warm_indices',
        python_callable=to_warm,
        op_kwargs={'target_indices_pattern': '^(test|feed)-\\d{6}$', 'days': 3}
    )

    kickoff >> t1_delete_indices >> t2_refresh_off >> t3_to_warm_indices
