#!/usr/bin/env python3
"""
Script to add 'nutracia' comment to all files in the repository
according to the appropriate comment format for each file type.
"""

import os
import re

def get_comment_format(filepath):
    """
    Returns the appropriate comment format based on file extension.
    """
    filename = os.path.basename(filepath)
    _, ext = os.path.splitext(filename)
    
    # File extension to comment format mapping
    comment_formats = {
        '.py': '# nutracia',
        '.js': '// nutracia',
        '.jsx': '// nutracia', 
        '.ts': '// nutracia',
        '.tsx': '// nutracia',
        '.css': '/* nutracia */',
        '.html': '<!-- nutracia -->',
        '.md': '<!-- nutracia -->',
        '.yml': '# nutracia',
        '.yaml': '# nutracia',
        '.json': '// nutracia',
        '.txt': '# nutracia',
        '.sh': '# nutracia',
        '.env': '# nutracia',
        '.gitignore': '# nutracia',
        '.gitconfig': '# nutracia',
        '.lock': '# nutracia',
        '.bak': '# nutracia'
    }
    
    # Special handling for specific filenames
    if filename == 'requirements.txt':
        return '# nutracia'
    elif filename == 'yarn.lock':
        return '# nutracia'
    elif filename == 'package.json':
        return '// nutracia'
    elif filename == 'craco.config.js':
        return '// nutracia'
    elif filename == 'postcss.config.js':
        return '// nutracia'
    elif filename == 'tailwind.config.js':
        return '// nutracia'
    elif filename.startswith('.'):
        return '# nutracia'
    
    return comment_formats.get(ext, '# nutracia')

def add_comment_to_file(filepath):
    """
    Add the nutracia comment to the beginning of the file.
    """
    try:
        comment = get_comment_format(filepath)
        
        # Read the current content
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if comment already exists
        if 'nutracia' in content.lower():
            print(f"Comment already exists in: {filepath}")
            return
        
        # Add comment at the beginning
        if content.strip():
            new_content = comment + '\n' + content
        else:
            new_content = comment + '\n'
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added comment to: {filepath}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    """
    Main function to process all files in the repository.
    """
    repo_path = '/app/Hackunited1'
    
    # Files to skip (binary files and specific patterns)
    skip_patterns = [
        '.git/',
        '.jpg', '.jpeg', '.png', '.ico', '.svg',
        '.mp4', '.avi', '.mov',
        '.pdf', '.zip', '.tar', '.gz',
        '.idx', '.pack'
    ]
    
    # Get all files in the repository
    all_files = []
    for root, dirs, files in os.walk(repo_path):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            filepath = os.path.join(root, file)
            
            # Check if we should skip this file
            should_skip = False
            for pattern in skip_patterns:
                if pattern in filepath:
                    should_skip = True
                    break
            
            if not should_skip:
                all_files.append(filepath)
    
    # Sort files for consistent processing
    all_files.sort()
    
    print(f"Found {len(all_files)} files to process")
    print("=" * 50)
    
    # Process each file
    for filepath in all_files:
        add_comment_to_file(filepath)
    
    print("=" * 50)
    print("Finished adding 'nutracia' comments to all files!")

if __name__ == '__main__':
    main()