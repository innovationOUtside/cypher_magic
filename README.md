# `cypher magic`

Really simple IPython magic for running cypher commands.

__For an updated, improved and extended version of this magic, see https://github.com/petehughes/cypher_magic__

At the moment the ability to connect to arbitrary neo4j databases is limited - the only configurable connection parameter currently available is the password.

For a demo, see: [psychemedia/binder-neo4j](https://github.com/psychemedia/binder-neo4j).

Install via:

- `pip install .`
- `pip install --upgrade git+https://github.com/innovationOUtside/cypher_magic.git`

This magic was developed to work by default inside a MyBinder container containing a Neo4j server running on default ports with user `neo4j` and password `neo4jbinder`.

Load the magic with:

`%load_ext cypher_magic`

The magic allows you to run Cypher commands against the connected database using default credentials (the default password is set to `neo4jbinder`). You can change the password with the `-p`/`--password` variable; the `-q` flag suppresses the cell output.

```
%cypher -r
%cypher -q -p neo4jbinder
```

Call as line magic `%cypher` or block magic: `%%cypher`

The line magic is perhaps most useful when called with a query passed via a variable. For example:

```
q='MATCH (p:Person) RETURN p.name AS name'
%cypher -v q
```

the magic will return a `pandas` dataframe by default. Other return formats, set using the `-o`/`--output` parameter, include `table` and `matrix` (the latter requires `sympy` to be installed).
