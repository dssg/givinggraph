`giving_schema.sql` contains our MySQL database schema, as created by `dump.sh`. 

To create an empty database based on this schema, run:
```
mysql -h mydatabasehost -u user -ppasswd giving < schema
```

`queries` contains a number of SQL queries used to support various [API](https://github.com/dssg/givinggraph/wiki/API) calls
