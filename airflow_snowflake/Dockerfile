FROM apache/airflow:2.1.3
RUN python -m pip install --upgrade pip
# RUN pip install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.5.1/tested_requirements/requirements_36.reqs
RUN pip install snowflake-connector-python
RUN pip install 'apache-airflow[snowflake]'
