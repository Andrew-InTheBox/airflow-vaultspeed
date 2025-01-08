import json
import time
import re
import requests

from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException
from requests.auth import HTTPBasicAuth


class LivyHook(BaseHook):
	"""
	This hook is a wrapper around the Apache Livy API for Spark.
	
	:param conn_id: connection_id string
	:type conn_id: str
	"""
	
	conn_name_attr = 'spark_conn_id'
	default_conn_name = 'spark_sql_default'
	conn_type = 'spark_sql_livy'
	hook_name = 'Spark Livy VaultSpeed'
	
	@staticmethod
	def get_ui_field_behaviour():
		"""Returns custom field behaviour"""
		return {
			"hidden_fields": ['port', 'schema'],
			"relabeling": {},
			"placeholders": {
				'host': 'url of the livy API',
				'login': 'user name',
				'password': 'password',
				'extra': 'Additional properties for session creation (JSON format) see https://livy.incubator.apache.org/docs/latest/rest-api.html for all options'
			},
		}
	
	def __init__(self, conn_id='spark_sql_default'):
		super(LivyHook, self).__init__()
		self.conn_id = conn_id
		
		_conn = self.get_connection(self.conn_id)
		self._host = _conn.host
		self._login = _conn.login
		self._password = _conn.password
		self._extra = _conn.extra_dejson
		self.headers = {'Content-Type': 'application/json'}
	
	def create_session(self):
		data = {'kind': 'sql'}
		if self._extra:
			data.update(self._extra)
		r = requests.post(f"{self._host}/sessions", data=json.dumps(data), headers=self.headers,
		                  auth=HTTPBasicAuth(self._login, self._password))
		self.check_response(r)
		session_id = r.json()['id']
		
		while True:
			r = requests.get(f"{self._host}/sessions/{session_id}", headers=self.headers,
			                 auth=HTTPBasicAuth(self._login, self._password))
			self.check_response(r)
			if r.json()['state'] == "idle":
				break
			elif r.json()['state'] in ("shutting_down", "error", "dead", "killed", "success"):
				raise AirflowException(f"Unable to start session.")
			time.sleep(5)
		return session_id
	
	def get_state(self, session_id, statement_id):
		r = requests.get(f"{self._host}/sessions/{session_id}/statements/{statement_id}",
		                 headers=self.headers, auth=HTTPBasicAuth(self._login, self._password))
		self.check_response(r)
		out = r.json()
		state = out['state']
		message = ""
		if out['output']:
			if out['output']['status'] == 'error':
				# If a statement fails, the state will be available, only the output status is error, so update state accordingly
				state = 'error'
				message = f"Error: {out['output']['evalue']}Traceback: {out['output']['traceback']}"
		return state, message
	
	def stop_session(self, session_id):
		r = requests.delete(f"{self._host}/sessions/{str(session_id)}", headers=self.headers,
		                    auth=HTTPBasicAuth(self._login, self._password))
		self.check_response(r)
	
	def run_statement(self, session_id, sql):
		data = {'code': sql}
		r = requests.post(f"{self._host}/sessions/{str(session_id)}/statements", data=json.dumps(data),
		                  headers=self.headers, auth=HTTPBasicAuth(self._login, self._password))
		self.check_response(r)
		return r.json()['id']
	
	def run(self, sql):
		if not isinstance(sql, list):
			sql = [sql]
		else:
			sql = sql
		# Only 1 SQL statement can be run at a time, so split the input script(s) into single statements
		sql_statements = [sp for s in sql for sp in re.split(r";\s*\n", s.strip())]
		self.log.info(f"Running {len(sql_statements)} statements.")
		
		session_id = self.create_session()
		
		for i, s in enumerate(sql_statements):
			statement_id = self.run_statement(session_id, s)
			
			while True:
				state, message = self.get_state(session_id, statement_id)
				if state == "available":
					self.log.info(f"Statement number {i} completed.")
					break
				elif state in ("error", "cancelled"):
					self.log.error(f"Statement {s} failed: \n{message}")
					self.stop_session(session_id)
					raise AirflowException(f"Statement {s} failed: {message}")
				time.sleep(5)
		
		self.log.info(f"All statements executed successfully.")
		self.stop_session(session_id)
	
	def check_response(self, response):
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError:
			self.log.error("HTTP error: %s", response.reason)
			self.log.error(response.text)
			raise AirflowException(str(response.status_code) + ":" + response.reason)
