from IPython.core.magic import magics_class, line_cell_magic, Magics, line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.core.display import HTML

from warnings import warn

from py2neo import Graph

from .drawGraph import draw, init_notebook_mode
# import json

DEFAULT_PWD='password'
DEFAULT_USERNAME='neo4j'
DEFAULT_SERVER='bolt://localhost'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@magics_class
class CypherMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(CypherMagic, self).__init__(shell)
        self.graph = None
        self.hasdLoadedJS = False

    @line_magic
    def cypherInclude(self, line):
        if(not self.hasdLoadedJS):
            self.hasdLoadedJS = True;
            init_notebook_mode();



    @line_cell_magic
    @magic_arguments()
    @argument('--password', '-p', default=None, help='Database password')
    @argument('--userName', '-u', default=None, help='Database password')
    @argument('--server', '-s', default=None, help='Database password')
    
    @argument('-q', '--quiet', default=False, action='store_true',
              help='Suppress output from cell.')
    @argument('-o', '--output', default=None)
    @argument('-oo', '--outputOptions', default=None)
    @argument('-v', '--variable', default=None)
    @argument('-r','--reset', default=False, action='store_true')
    @argument("query", type=str, nargs='*', help="Cypher query")
    def cypher(self,line, cell=''):
        '''Run cypher commands commands.'''
        args = parse_argstring(self.cypher, line)
        if args.variable:
            cell = self.shell.user_ns[args.variable]
        pwd = DEFAULT_PWD if args.password is None else args.password
        userName = DEFAULT_USERNAME if args.userName is None else args.userName
        host = DEFAULT_SERVER if args.server is None else args.server
        output_type = args.output
        outputOptions = args.outputOptions;
  
        if args.reset:
            self.graph = None
            print("Neo4j database connection reset...")
            return
        
        if self.graph is None or args.password is not None or args.userName is not None or args.server is not None:
            try:
                # self.graph = Graph(password=pwd, host = args.server, user = args.userName)
                self.graph = Graph(host, auth=(userName, pwd))
                if(self.graph):
                    print("Neo4j database connection established... " + self.graph.service.uri)
                else:
                    print("Error establishing connection...")
            except:
                print( bcolors.FAIL + "Error connecting server called: " + host )
                print("\tcheck the server is running")
                print("\tcheck you are connected to the VPN (in needed)")
                print("\tcor change the host name with the --server/-s option" + bcolors.FAIL)
                return

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
            if(outputOptions is None):
                warn("no output options were given please use the --oo option")
            
            if(not self.hasdLoadedJS):
                self.hasdLoadedJS = True;
                init_notebook_mode();
                
            if( isinstance(outputOptions, str) ):
                import ast
                outputOptions = ast.literal_eval(outputOptions)
                
            response = draw(_response, outputOptions)
            
        else:
            response = _response.to_data_frame()

        return response

#ip = get_ipython()
#ip.register_magics(CypherMagic)