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
    @argument('--password', '-p',
          default=None,
          help='Database password'
    )
    @argument('-q', '--quiet', default=False, action='store_true',
              help='Suppress output from cell.')
    @argument('-o', '--output', default=None)
    @argument('-v', '--variable', default=None)
    @argument('-r','--reset', default=False, action='store_true')
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
        
        if self.graph is None or args.password is not None:
            print(f'Accessing graph database with password: {pwd}')
            self.graph = Graph(password=pwd)
        
        _response = self.graph.run(cell)
        
        if args.quiet:
            return

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
        else:
            response = _response.to_data_frame()

        return response

#ip = get_ipython()
#ip.register_magics(CypherMagic)