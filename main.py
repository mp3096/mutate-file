import ast
import random

def mutate_function(node, junk_param_name):
    if isinstance(node, ast.FunctionDef):
        # Add a junk parameter with a randomized name
        junk_param_name = f'junk_param_{random.randint(1, 100)}'
        node.args.args.append(ast.arg(arg=junk_param_name, annotation=None))
        
        for child_node in ast.walk(node):
            if isinstance(child_node, ast.Call):
                # Add the junk parameter to function calls
                child_node.args.append(ast.Name(id=junk_param_name, ctx=ast.Load()))
            
            if isinstance(child_node, ast.Assign):
                # Create a new variable with a randomized name
                temp_var_name = f'temp_{random.randint(1, 100)}'
                new_variable = ast.Name(id=temp_var_name, ctx=ast.Store())
                assignment = ast.Assign(targets=[new_variable], value=child_node.value)
                # Modify assignment to use the new variable and junk parameter
                child_node.value = ast.BinOp(left=new_variable, op=ast.Sub(), right=ast.Name(id=junk_param_name, ctx=ast.Load()))
                node.body.insert(node.body.index(child_node), assignment)
        
        # Add a random if statement that is always true
        random_if = ast.If(test=ast.Constant(value=True), body=[ast.Pass()], orelse=[])
        node.body.append(random_if)
        
    return node, junk_param_name

def mutate_code(input_file, output_file):
    with open(input_file, 'r') as file:
        code = file.read()

    tree = ast.parse(code)
    mutated_tree = ast.fix_missing_locations(ast.NodeTransformer().visit(tree))
    
    # Generate a new random junk parameter name
    junk_param_name = None
    mutated_tree, junk_param_name = mutate_function(mutated_tree, junk_param_name)

    mutated_code = compile(mutated_tree, filename='<ast>', mode='exec')

    with open(output_file, 'w') as file:
        file.write(code)

if __name__ == "__main__":
    input_file = input("Enter the name of the input Python file: ")
    output_file = input("Enter the name of the output Python file: ")

    mutate_code(input_file, output_file)
