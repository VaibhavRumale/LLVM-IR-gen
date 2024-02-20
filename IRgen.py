from llvmlite import ir
from lexer import tokenize  # Ensure lexer.py is correctly imported

input_string = """
let x = 10
print x
"""

# Initialize LLVM module and builder
module = ir.Module(name="tiny_calc_module")
builder = None

# Setup the main function and entry block
func_ty = ir.FunctionType(ir.VoidType(), [])
main_func = ir.Function(module, func_ty, name="main")
block = main_func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

# Setup printf function
printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
printf = ir.Function(module, printf_ty, name="printf")

# Variable storage
variables = {}

# Token processing
tokens_iter = tokenize(input_string)
tokens = iter(tokens_iter)

def process_tokens(tokens):
    global builder
    for token_type, token_value in tokens:
        if token_type == 'LET':
            var_name = next(tokens)[1]  # Get variable name
            # Assume the value is always an integer for simplicity
            value_token = next(tokens)  # Move past 'EQUALS'
            value = int(next(tokens)[1])  # Get the value
            var_addr = builder.alloca(ir.IntType(32), name=var_name)
            builder.store(ir.Constant(ir.IntType(32), value), var_addr)
            variables[var_name] = var_addr
        elif token_type == 'PRINT':
            var_name = next(tokens)[1]
            if var_name in variables:
                var_addr = variables[var_name]
                value = builder.load(var_addr)
                fmt_str = ir.GlobalVariable(module, ir.ArrayType(ir.IntType(8), len("%d\n\0")), name="fmt")
                fmt_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len("%d\n\0")), bytearray("%d\n\0".encode("utf8")))
                fmt_str.global_constant = True
                fmt_str_ptr = builder.gep(fmt_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)], inbounds=True)
                builder.call(printf, [fmt_str_ptr, value])
        # Add more token processing as needed

process_tokens(tokens)

builder.ret_void()

print(module)
