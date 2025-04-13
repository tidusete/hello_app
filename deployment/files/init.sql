apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-init-sql
data:
  init.sql: |
    CREATE TABLE IF NOT EXISTS users (
      username TEXT PRIMARY KEY,
      date_of_birth DATE NOT NULL
    );
