import os

def generate_directory_structure(startpath, output_file=None, max_depth=None):
    """
    Generate a directory structure starting from startpath.
    
    Args:
        startpath (str): Path to the directory to scan
        output_file (str, optional): File to save the structure to. If None, prints to console.
        max_depth (int, optional): Maximum depth to traverse. None for unlimited.
    """
    structure = []
    
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if max_depth is not None and level > max_depth:
            continue
            
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{subindent}{f}")
    
    result = "\n".join(structure)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Directory structure saved to {output_file}")
    else:
        print(result)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate directory structure')
    parser.add_argument('path', type=str, help='Path to the directory to scan')
    parser.add_argument('-o', '--output', type=str, help='Output file path')
    parser.add_argument('-d', '--depth', type=int, help='Maximum depth to scan')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a valid directory")
    else:
        generate_directory_structure(args.path, args.output, args.depth)