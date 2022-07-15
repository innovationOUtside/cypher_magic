# `cypher magic`

Based on the code from https://github.com/innovationOUtside/cypher_magic.git but now more complete .

- `pip install --upgrade git+https://github.com/petehughes/cypher_magic.git`

Load the magic with:

`%load_ext cypher_magic`

The magic allows you to run Cypher commands against the connected database using default credentials
You can set the host name of the neo4j using the `-s`/`--server` variable. default is `localhost`
You can set the username with the `-u`/`--userName` variable. default is `neo4j`
You can change the password with the `-p`/`--password` variable.
the `-q` flag suppresses the cell output.
the `-o`/`--output` set the output type:
`default`: `pandas` dataframe
`raw`: response from the `py2neo`
`table`,
`matrix` - requires `sympy`
`graph`

```
%cypher -r
%cypher -q -p password -u neo4j -s localhost
```

Call as line magic `%cypher` or block magic: `%%cypher`

```
p = %cypher -o table MATCH (p:Person) RETURN p.name AS name
```

or

```
%%cypher -o table
MATCH (p:Person)
RETURN p.name AS name
```

the magic will return a `pandas` dataframe by default. Other return formats, set using the `-o`/`--output` parameter, include `table` and `matrix` (the latter requires `sympy` to be installed).

## graph output options:

the graph output can be tailored by using a number of options:

```
{
    "label of node or type of edge": "attribute name to use to describe it"
}
```

eg

```
{"Person":"FullName" }
```

complex:
the graph output can be tailored by using a number of options:

```
{
    "label of node or type of edge": {
        "label":"attribute name to use to describe it",
        "opacity":"the opacity",
        "width":"the width of the relationship line", // relationship only
        "color": "the colour",
        "colorValue": "the value in the relationship that defines the color",
        "image": "url to the image" // node only
        "shape": "the type of shape" // node only
        "noArrows": "remove all the arrows from showing" // relationship only
    }
}
```
