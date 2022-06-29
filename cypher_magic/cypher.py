from IPython.core.magic import magics_class, line_cell_magic, Magics
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.core.display import HTML

from warnings import warn

from py2neo import Graph

DEFAULT_PWD='neo4jbinder'


@magics_class
class CypherMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(CypherMagic, self).__init__(shell)
        self.graph = None

    @line_cell_magic
    @magic_arguments()
    @argument('--password', '-p', default=None, help='Database password')
    @argument('--userName', '-u', default=None, help='Database password')
    @argument('--server', '-s', default=None, help='Database password')
    
    @argument('-q', '--quiet', default=False, action='store_true',
              help='Suppress output from cell.')
    @argument('-o', '--output', default=None)
    @argument('-v', '--variable', default=None)
    @argument('-r','--reset', default=False, action='store_true')
    @argument("query", type=str, nargs='*', help="Cypher query")
    def cypher(self,line, cell=''):
        '''Run cypher commands commands.'''
        args = parse_argstring(self.cypher, line)
        if args.variable:
            cell = self.shell.user_ns[args.variable]
        pwd = DEFAULT_PWD if args.password is None else args.password

        output_type = args.output
        
        if args.reset:
            self.graph = None
            print("Neo4j database connection reset...")
            return
        
        if self.graph is None or args.password is not None or args.userName is not None or args.server is not None:
            self.graph = Graph(password=pwd, host = args.server, user = args.userName)
            if(self.graph):
                print("Neo4j database connection established... " + self.graph.service.uri)
            else:
                print("Error establishing connection...")
        
        # if not cell:
            # return self.graph.run(line)
        
        
        
        if args.quiet or (not cell and not args.query):
            return
        query = cell or ' '.join(args.query)
        # print(query)
        _response = self.graph.run(query)
        
        if output_type is None:
            response = _response.to_data_frame()
        elif output_type=='matrix':
            try:
                import sympy
                response = _response.to_matrix()
            except ModuleNotFoundError:
                warn("You need to install sympy to return a matrix.")
                response = None
        elif output_type=='table':
            response = _response.to_table()
        elif output_type=='raw':
            response = _response
        elif output_type=='graph':
            try:
                import networkx
                import matplotlib

                g = _response.data()
                
                response = networkx.draw(g)
            except ModuleNotFoundError:
                warn("You need to install networkx to return a matrix.")
                response = None
        
        else:
            response = _response.to_data_frame()

        return response

#ip = get_ipython()
#ip.register_magics(CypherMagic)