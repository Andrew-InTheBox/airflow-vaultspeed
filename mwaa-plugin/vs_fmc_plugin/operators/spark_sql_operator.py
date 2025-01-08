from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class SparkSqlOperator(BaseOperator):
    """
    Execute Spark SQL query

    :param sql: The SQL query to execute. (templated)
    :type sql: str
    :param conn_id: connection_id string
    :type conn_id: str
    :param name: Name of the job
    :type name: str
    :param verbose: Whether to pass the verbose flag to spark-sql
    :type verbose: bool
    """

    template_fields = ["_sql"]

    template_ext = [".sql", ".hql"]

    @apply_defaults
    def __init__(self,
                 sql,
                 spark_conn_id='spark_sql_default',
                 name=None,
                 verbose=True,
                 *args,
                 **kwargs):
        super(SparkSqlOperator, self).__init__(*args, **kwargs)
        self._sql = sql
        self._conn_id = spark_conn_id
        self._name = name or self.task_id
        self._verbose = verbose
        self._hook = None

        from airflow.models.connection import Connection
        self._conn_type = Connection.get_connection_from_secrets(spark_conn_id).conn_type

    def execute(self, context):
        """
        Call the hook matching the selected connection type
        """
        if self._conn_type == 'spark_sql_vs':
            from vs_fmc_plugin.hooks.spark_sql_hook import SparkSqlHook
            self._hook = SparkSqlHook(sql=self._sql,
                                      conn_id=self._conn_id,
                                      name=self._name,
                                      verbose=self._verbose
                                      )
            self._hook.run()
            
        elif self._conn_type == 'jdbc':
            from vs_fmc_plugin.hooks.jdbc_hook import JdbcHook
            self._hook = JdbcHook(jdbc_conn_id=self._conn_id)
            self._hook.run(self._sql)
            
        elif self._conn_type == 'spark_sql_livy':
            from vs_fmc_plugin.hooks.livy_hook import LivyHook
            self._hook = LivyHook(conn_id=self._conn_id)
            self._hook.run(self._sql)
            
        else:
            raise Exception(f"The connection {self._conn_id} of type {self._conn_type} can not be used to execute Spark SQL.")

    def on_kill(self):
        self._hook.kill()
