# Mariadb-Command2Python
Mariadb-execution by Python
```
import mysql.connector  => pip install mysql-connector
import pandas  => pip install pandas
import sys
import signal
```
## DataBase:
|SQL|Python|
|:--:|:--:|
|show databases;|database?|
|use <database_name>;|change_db <database_name>|
|CREATE DATABASE <database_name>;|create_db <database_name>|
|DROP DATABASE <database_name>;|delete_db <database_name>|
## Table:
|SQL|Python|
|:--:|:--:|
|show tables;|table?|
|SHOW INDEX FROM <table_name>;|table_info <table_name>|
|CREATE TABLE IF NOT EXISTS <table_name>(<column_name column_type>);|create_table <new_table_name> <column_name column_type>|
|Drop TABLE <table_name>;|delete_table <table_name>|
## Column:
|SQL|Python|
|:--:|:--:|
|desc <table_name>;|column_info <table_name>|
|SELECT <column_name> FROM <table_name> <person_filte>[default: column = \'\*\' filte = '']; | column_db? <table_name> <column_name,column_name ....> <person_filte>[default: column = \'\*\' filte = ''] |
|INSERT INTO <table_name> (<column_names>) VALUES <column_values>;|add_data <table_name> <column_names> <column_values>|
|DELETE FROM <table_name> WHERE <delete_column_name>={delet_values};| delete_data <table_name> <column_name> <column_value> |
|UPDATE <table_name> SET <update_column_name>=<update_column_value> WHERE <find_column>=<find_column_value>;|update_db <table_name> <update_column_name> <update_column_valu> <find_column> <find_column_value>|
## Other:
|SQL|Python|
|:--:|:--:|
|SELECT USER();|whoiam|
|show processlist;|processlist|
