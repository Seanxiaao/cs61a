"""A Scheme interpreter and its read-eval-print loop."""

from scheme_primitives import *
from scheme_reader import *
from ucb import main, trace

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line("(+ 2 2)")
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # Combinations
    if not scheme_listp(expr):
        raise SchemeError("malformed list: {0}".format(str(expr)))
    first, rest = expr.first, expr.second
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        result = SPECIAL_FORMS[first](rest, env)
    else:
        procedure = scheme_eval(first, env)
        if not scheme_procedurep(procedure):
            raise SchemeError("cannot call: {0}".format(str(procedure)))
        result = procedure.eval_call(rest, env)
    return result

def self_evaluating(expr):
    """Return whether EXPR evaluates to itself."""
    return scheme_atomp(expr) or scheme_stringp(expr) or expr is None

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    if not scheme_procedurep(procedure):
        raise SchemeError("cannot call: {0}".format(str(procedure)))
    return procedure.apply(args, env)

def eval_all(expressions, env):
    """Evaluate a Scheme list of EXPRESSIONS & return the value of the last."""
    # BEGIN Question 7
    if expressions == nil:
        return None
    while expressions.second != nil:
        scheme_eval(expressions.first, env)
        expressions = expressions.second
    return scheme_eval(expressions.first, env)
    # END Question 7

################
# Environments #
################

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with a PARENT frame (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return "<Global Frame>"
        else:
            s = sorted(('{0}: {1}'.format(k,v) for k,v in self.bindings.items()))
            return "<{{{0}}} -> {1}>".format(', '.join(s), repr(self.parent))

    def lookup(self, symbol):
        """Return the value bound to SYMBOL.  Errors if SYMBOL is not found."""
        # BEGIN Question 3
        if not symbol in self.bindings:
            if self.parent != None:
                if symbol in self.parent.bindings:
                    return self.parent.bindings[symbol]
                else:
                    return self.parent.lookup(symbol)
        else:
            return self.bindings[symbol]
        # END Question 3
        raise SchemeError("unknown identifier: {0}".format(symbol))

    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Raise an error if too many or too few
        vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line("(a b c)"), read_line("(1 2 3)")
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        child = Frame(self) # Create a new child with self as the parent
        # BEGIN Question 10
        if len(formals) != len(vals):
            raise SchemeError
        else:
            python_formals , python_vals= [], []
            while formals is not nil:
                python_formals.append(formals.first)
                python_vals.append(vals.first)
                formals = formals.second
                vals = vals.second
            i = 0
            while i < len(python_formals):
                child.bindings.setdefault(python_formals[i],python_vals[i])
                i += 1
        # END Question 10
        return child

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        self.bindings[symbol] = value

##############
# Procedures #
##############

class Procedure:
    """The supertype of all Scheme procedures."""

    def eval_call(self, arg_exprs, env, tail=False):
        """Evaluate a call to me with ARG_EXPRS (a Scheme list of unevaluated
        Scheme expressions) as arguments.  If TAIL is true, evaluate as
        in a tail context (unused in this default version)."""
        args = arg_exprs.map(lambda operand: scheme_eval(operand, env))
        return scheme_apply(self, args, env)

class PrimitiveProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='primitive'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{}]'.format(self.name)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list.

        >>> env = create_global_frame()
        >>> plus = env.bindings["+"]
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        # Convert a Scheme list to a Python list
        python_args = []
        while args is not nil:
            python_args.append(args.first)
            args = args.second
        # BEGIN Question 4
        if self.use_env == True:
            python_args.append(env)
        try:
            return self.fn(*python_args)
        except TypeError:
            raise SchemeError('error fucntion call')



        # END Question 4
class UserDefinedProcedure(Procedure):
    """A procedure defined by an expression."""

    def apply(self, args, env):
        """Apply me to argument values ARGS (a Scheme list) in
        environment ENV."""
        new_env = self.make_call_frame(args, env)
        return eval_all(self.body, new_env)

class LambdaProcedure(UserDefinedProcedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        a Scheme list of BODY expressions, and a parent environment that
        starts with Frame ENV.
        """
        self.formals = formals
        self.body = body
        self.env = env

    def make_call_frame(self, args, env):
        """Make a frame that binds the my formal parameters to ARGS, a
        Scheme list of values, for a call evaluated in environment env."""
        # BEGIN Question 12
        call_frame = Frame.make_child_frame(self.env,self.formals,args)
        return call_frame
        # END Question 12
        #which is needed by the apply method defined in UserDefinedProcedure.
        #It should create a new Frame instance using the make_child_frame method of the appropriate parent frame,
        #binding formal parameters to argument values.

    def __str__(self):
        return str(Pair("lambda", Pair(self.formals, self.body)))

    def __repr__(self):
        return "LambdaProcedure({!r}, {!r}, {!r})".format(
            self.formals, self.body, self.env)


def add_primitives(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as primitive procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, PrimitiveProcedure(fn, name=proc_name))

def scheme_procedurep(x):
    return isinstance(x, Procedure)

#################
# Special forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special
# form as its first argument---a Scheme list representing a special form
# without the initial identifying symbol (if, lambda, quote, ...).  Its
# second argument is the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form."""
    check_form(expressions, 2)
    target = expressions.first
    if scheme_symbolp(target):
        check_form(expressions, 2, 2)
        # BEGIN Question 5A
        env.define(target,scheme_eval(expressions.second.first, env))
        return target
        # END Question 5A
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN Question 9A
        env.define(target.first,LambdaProcedure(target.second,expressions.second, env))
        return target.first
        # END Question 9A
    else:
        bad = target.first if isinstance(target, Pair) else target
        raise SchemeError("Non-symbol: {}".format(bad))

def do_quote_form(expressions, env):
    """Evaluate a quote form."""
    check_form(expressions, 1, 1)
    # BEGIN Question 6B
    return expressions.first
    # END Question 6B

def do_begin_form(expressions, env):
    """Evaluate begin form."""
    check_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form."""
    check_form(expressions, 2)
    formals = expressions.first
    check_formals(formals)
    # BEGIN Question 8
    return LambdaProcedure(expressions.first, expressions.second, env)
    # END Question 8

def do_if_form(expressions, env):
    """Evaluate an if form."""
    check_form(expressions, 2, 3)
    # BEGIN Question 13
    if scheme_true(scheme_eval(expressions.first,env)):
        return scheme_eval(expressions.second.first,env)
    else:
        if len(expressions) == 2:
            return None
        else:
            return scheme_eval(expressions.second.second.first,env)
    # END Question 13

def do_and_form(expressions, env):
    """Evaluate a short-circuited and form."""
    # BEGIN Question 14B
    if expressions == nil:
        return True
    else:
        if expressions.second == nil:
            return scheme_eval(expressions.first, env)
        else:
            if scheme_true(scheme_eval(expressions.first, env)):
                return do_and_form(expressions.second, env)
            else:
                return False
    # END Question 14B

def do_or_form(expressions, env):
    """Evaluate a short-circuited or form."""
    # BEGIN Question 14B
    if expressions == nil:
        return False
    else:
        if scheme_true(scheme_eval(expressions.first, env)):
            return scheme_eval(expressions.first, env)
        else:
            return do_or_form(expressions.second, env)
    # END Question 14B

def do_cond_form(expressions, env):
    """Evaluate a cond form."""
    num_clauses = len(expressions)
    i = 0
    while expressions is not nil:
        clause = expressions.first
        check_form(clause, 1)
        if clause.first == "else":
            if i < num_clauses-1:
                raise SchemeError("else must be last")
            test = True
        # BEGIN Question 15A
        else:
            test = scheme_eval(clause.first, env)
        if scheme_true(test):
            if clause.second:
                return eval_all(clause.second, env)
            else:
                return test
        # END Question 15A
        expressions = expressions.second
        i += 1

def do_let_form(expressions, env):
    """Evaluate a let form."""
    check_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.second, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of env that contains the definitions given
    in bindings.  The Scheme list bindings must have the form of a proper
    bindings list in a let expression: each item must be a list containing
    a symbol and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError("bad bindings list in let form")
    # BEGIN Question 16
    names, values = nil, nil
    while bindings != nil:
        binding = bindings.first
        check_form(binding, 2, 2)
        if not scheme_symbolp(binding.first):
            raise SchemeError('bad argument name')
        names = Pair(binding.first, names)
        values = Pair(scheme_eval(binding.second.first, env), values)
        bindings = bindings.second
    return Frame.make_child_frame(env,names,values)
    # END Question 16

SPECIAL_FORMS = {
    "and": do_and_form,
    "begin": do_begin_form,
    "cond": do_cond_form,
    "define": do_define_form,
    "if": do_if_form,
    "lambda": do_lambda_form,
    "let": do_let_form,
    "or": do_or_form,
    "quote": do_quote_form,
}

# Utility methods for checking the structure of Scheme programs

def check_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.
    """
    if not scheme_listp(expr):
        raise SchemeError("badly formed expression: " + str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError("too few operands in form")
    elif length > max:
        raise SchemeError("too many operands in form")

def check_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a well-formed list of symbols or if any symbol is repeated.

    >>> check_formals(read_line("(a b c)"))
    """
    # BEGIN Question 11B
    formallist = []
    while formals != nil:
        formallist.append(formals.first)
        formals = formals.second

    for formal in formallist:
        if not scheme_symbolp(formal):
            raise SchemeError('not valid symbol')
    if len(set(formallist)) != len(formallist):
        raise SchemeError('symbols have duplications')
    # END Question 11B

#################
# Dynamic Scope #
#################

class MuProcedure(UserDefinedProcedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and a
        Scheme list of BODY expressions.
        """
        self.formals = formals
        self.body = body

    # BEGIN Question 17
    def make_call_frame(self, args, env):
        call_frame = Frame.make_child_frame(env,self.formals,args)
        return call_frame
    # END Question 17

    def __str__(self):
        return str(Pair("mu", Pair(self.formals, self.body)))

    def __repr__(self):
        return "MuProcedure({!r}, {!r})".format(self.formals, self.body)


def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    check_form(expressions, 2)
    formals = expressions.first
    check_formals(formals)
    # BEGIN Question 17
    return MuProcedure(expressions.first, expressions.second)
    # END Question 17

SPECIAL_FORMS["mu"] = do_mu_form


##################
# Tail Recursion #
##################

class Evaluate:
    """An expression EXPR to be evaluated in environment ENV."""
    def __init__(self, expr, env):
        self.expr = expr
        self.env = env

# The following utility method is not needed for the main part of Project 4,
# but may be of use in some of the extensions.
def complete_eval(val):
    """If VAL is an Evaluate, returns the result evaluating its
    its expression part. Otherwise, simply returns VAL."""
    if isinstance(val, Evaluate):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def scheme_optimized_eval(expr, env, tail=False):
    """Evaluate Scheme expression EXPR in environment ENV.
    If TAIL, returns an Evaluate object containing an expression
    for further evaluation."""
    # Evaluate Atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    if tail:
        # BEGIN Extra Credit
        if expr is None:
            raise SchemeError
        nexteva = Evaluate(complete_eval(expr),env)
        return nexteva.scheme_optimized_eval()
        # END Extra Credit
    else:
        result = Evaluate(expr, env)

    while isinstance(result, Evaluate):
        expr, env = result.expr, result.env
        # All non-atomic expressions are lists (combinations)
        if not scheme_listp(expr):
            raise SchemeError("malformed list: {0}".format(str(expr)))
        first, rest = expr.first, expr.second
        if (scheme_symbolp(first) and first in SPECIAL_FORMS):
            result = SPECIAL_FORMS[first](rest, env)
        else:
            procedure = scheme_eval(first, env)
            if not scheme_procedurep(procedure):
                raise SchemeError("cannot call: {0}".format(str(procedure)))
            result = procedure.eval_call(rest, env)
    return result

################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
# scheme_eval = scheme_optimized_eval


################
# Input/Output #
################

def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=()):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(result)
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if (isinstance(err, RuntimeError) and
                'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print("Error: maximum recursion depth exceeded")
            else:
                print("Error:", err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print("KeyboardInterrupt")
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return

def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or (SYM,
    QUIET, ENV). The file named SYM is loaded in environment ENV, with verbosity
    determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    check_type(sym, scheme_symbolp, 0, "load")
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet)

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define("eval", PrimitiveProcedure(scheme_eval, True))
    env.define("apply", PrimitiveProcedure(scheme_apply, True))
    env.define("load", PrimitiveProcedure(scheme_load, True))
    env.define("procedure?", PrimitiveProcedure(scheme_procedurep))
    env.define("undefined", None)
    add_primitives(env, PRIMITIVES)
    return env

@main
def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='CS 61A Scheme interpreter')
    parser.add_argument('-load', '-i', action='store_true',
                       help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()
            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()
