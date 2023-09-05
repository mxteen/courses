# Импорт библиотек
import numpy as np
import pandas as pd
import pandahouse as ph

from airflow import DAG
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta
from io import StringIO
import requests

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context

# Дефолтные параметры, которые идут в задачи Airflow
default_args = {
    'owner': 'mxter',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 8, 10),
}

# Интервал запуска DAG
schedule_interval = '0 23 * * *'

# Cоединения с базой
read_connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'database':'simulator_20230720',
    'user':'********',  # вставить имя пользователя
    'password':'********'  # вставить пароль
}

write_connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'database':'test',
    'user':'********',  # вставить имя пользователя
    'password':'********'  # вставить пароль
}


# DAG
@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False)
def etl_mxter():
    """
    DAG в airflow, который будет считаться каждый день за вчера.

    Параллельно будем обрабатывать две таблицы. 
    1. В feed_actions для каждого юзера посчитаем число просмотров и лайков контента. 
    2. В message_actions для каждого юзера считаем
        * сколько он получает сообщений;
        * сколько он отсылает сообщений;
        * скольким людям он пишет;
        * сколько людей пишут ему.
    
    
    Далее объединяем две таблицы в одну.
    1. Для этой таблицы считаем все эти метрики в разрезе по полу, возрасту и ос. 
    2. И финальные данные со всеми метриками записываем в отдельную таблицу в ClickHouse.

    Каждый день таблица должна дополняться новыми данными.

    Структура финальной таблицы должна быть такая:
        Дата - event_date
        Название среза - dimension
        Значение среза - dimension_value
        Число просмотров - views
        Число лайков - likes
        Число полученных сообщений - messages_received
        Число отправленных сообщений - messages_sent
        От скольких пользователей получили сообщения - users_received
        Скольким пользователям отправили сообщение - users_sent
        Срез - это os, gender и age
    """

    @task()
    def extract_feed():
        """
        В feed_actions для каждого юзера посчитаем число просмотров и лайков контента.
        Испытание запроса: https://redash.lab.karpov.courses/queries/35978
        """
        query = '''
            SELECT
                user_id AS user,
                gender,
                age,
                os,
                DATE(time) as event_date,
                countIf(action='view') AS views,
                countIf(action='like') AS likes
            FROM 
                {db}.feed_actions
            WHERE
                event_date = today() - 1
            GROUP BY 
                 user, 
                 event_date,
                 gender,
                 age,
                 os
            '''
        df = ph.read_clickhouse(query, connection=read_connection)
        return df
    
    @task()
    def extract_msgs():
        """
        В message_actions для каждого юзера считаем
        * сколько он получает сообщений;
        * сколько он отсылает сообщений;
        * скольким людям он пишет;
        * сколько людей пишут ему.

        Испытание запроса: https://redash.lab.karpov.courses/queries/35919/
        """
        query = '''
            SELECT
                event_date,
                gender,
                age,
                user,
                os,
                message_sent,
                users_sent,
                message_received,
                users_received
            FROM
                (
                    -- сколько сообщений отправляет пользователь 
                    -- скольким людям пишет пользователь
                    SELECT
                        user_id AS user,
                        gender,
                        age,
                        os,
                        DATE(time) as event_date,
                        COUNT(reciever_id) AS message_sent,
                        COUNT(DISTINCT reciever_id) AS users_sent
                    FROM 
                        {db}.message_actions
                    WHERE 
                        event_date = today() - 1
                    GROUP BY 
                        user,
                        gender,
                        age,
                        os,
                        event_date
                ) AS qry_sent_msgs
                FULL OUTER JOIN
                (
                    -- сколько пользователь получает сообщений 
                    -- сколько людей пишет пользователю
                    SELECT
                        reciever_id AS user,
                        gender,
                        age,
                        os,
                        DATE(time) as event_date,
                        COUNT(user_id) AS message_received,
                        COUNT(DISTINCT user_id) AS users_received
                    FROM 
                        {db}.message_actions
                    WHERE 
                        event_date = today() - 1 
                    GROUP BY 
                        user,
                        gender,
                        age,
                        os,
                        event_date	
                ) AS qry_recieved_msgs
                USING user
            '''
        df = ph.read_clickhouse(query, connection=read_connection)
        return df
    
    @task()
    def join_dfs(df_msgs, df_feed):
        list_of_params = ['user', 'event_date', 'gender', 'age', 'os']
        # TODO: таокй ли тип объединения нам нужен? how = 'outer'?
        df = df_msgs.merge(df_feed, how = 'outer', on=list_of_params).dropna()
        return df

    metric_list = ['event_date', 'likes', 'views', 
                   'message_sent', 'message_received',
                   'users_sent', 'users_received']
    
    # Срез - это os, gender и age
    @task()
    def transform(df, metric):
        full_metric_list = metric_list + [metric]
        metrics_for_grouping = ['event_date'] + [metric]
        df_transformed = df[full_metric_list].groupby(metrics_for_grouping).sum().reset_index()
        df_transformed['dimension'] = metric
        df_transformed.rename(columns={metric: 'dimension_value'}, inplace=True)
        return df_transformed
       
    @task
    def transform_merge(df_gender, df_age, df_os):
        columns_in_order = [
            'event_date', 'dimension', 'dimension_value', 'views', 'likes',
            'message_received', 'message_sent', 'users_received', 'users_sent'
        ]
        df_concat = pd.concat([df_os, df_gender, df_age], axis=0, ignore_index=True)
        df = df_concat.astype({'views': 'uint32',
                               'likes': 'uint32',
                               'message_received': 'uint32',
                               'message_sent': 'uint32',
                               'users_received': 'uint32',
                               'users_sent': 'uint32'})
        return df[columns_in_order]

    @task()
    def load(df):
        query = '''
            CREATE TABLE IF NOT EXISTS test.mxter
                (
                event_date Date,
                dimension varchar(50),
                dimension_value varchar(50),
                views Float64,
                likes Float64,
                message_received Float64,
                message_sent Float64,
                users_received Float64,
                users_sent Float64
                ) ENGINE = MergeTree()
            ORDER BY event_date
        '''
        ph.execute(query, connection=write_connection) 
        ph.to_clickhouse(df, 'mxter', index=False, connection=write_connection)

    
    # Задачи внутри DAG
    # 1. Для каждого пользователя считаем число просмотров и лайков контента
    df_feed = extract_feed()
    
    # 2. Для каждого пользователя считаем метрики по сообщениям: полученные, отправленные
    df_msgs = extract_msgs()
    
    # 3. Объединяем таблицы df_msgs и df_feed
    df = join_dfs(df_msgs, df_feed)
    
    # 4. Делаем срезы по операционным системам, полу и возрасту
    df_os = transform_df(df, metric='os')
    df_gender = transform_df(df, metric='gender')
    df_age = transform_df(df, metric='age')
    
    # 4. Объединяем срезы в один датафрейм
    df_merged = transform_merge(df_gender=df_gender, df_age=df_age, df_os=df_os)
    
    # 5. Записываем данные в другую БД
    load(df_merged)

# вызываем DAG
dag_etl_mxter = etl_mxter()