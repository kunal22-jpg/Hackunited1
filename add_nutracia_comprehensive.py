#!/usr/bin/env python3
"""
Comprehensive script to add 'nutracia' comment to ALL files in the repository,
including binary files, git files, and any other file type.
"""

import os
import re
import mimetypes
import subprocess
from datetime import datetime

def is_binary_file(filepath):
    """Check if a file is binary by reading first few bytes."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except:
        return False

def get_file_type(filepath):
    """Determine file type and appropriate comment format."""
    filename = os.path.basename(filepath)
    _, ext = os.path.splitext(filename)
    
    # Check if it's a binary file
    if is_binary_file(filepath):
        return 'binary'
    
    # Text file comment formats
    comment_formats = {
        '.py': 'hash',
        '.js': 'slash',
        '.jsx': 'slash', 
        '.ts': 'slash',
        '.tsx': 'slash',
        '.css': 'css',
        '.html': 'html',
        '.md': 'html',
        '.yml': 'hash',
        '.yaml': 'hash',
        '.json': 'slash',
        '.txt': 'hash',
        '.sh': 'hash',
        '.env': 'hash',
        '.gitignore': 'hash',
        '.gitconfig': 'hash',
        '.lock': 'hash',
        '.bak': 'hash',
        '.svg': 'xml',
        '.xml': 'xml',
        '.sample': 'hash',
        '.ico': 'binary',
        '.mp4': 'binary',
        '.jpeg': 'binary',
        '.jpg': 'binary',
        '.png': 'binary'
    }
    
    # Special handling for specific filenames
    if filename in ['HEAD', 'config', 'description', 'index', 'packed-refs', 'exclude']:
        return 'hash'
    elif filename.startswith('.'):
        return 'hash'
    elif ext in comment_formats:
        return comment_formats[ext]
    else:
        return 'hash'  # Default to hash comment

def get_comment_text(file_type):
    """Get the appropriate comment text for file type."""
    comments = {
        'hash': '# nutracia',
        'slash': '// nutracia',
        'css': '/* nutracia */',
        'html': '<!-- nutracia -->',
        'xml': '<!-- nutracia -->',
        'binary': 'nutracia'
    }
    return comments.get(file_type, '# nutracia')

def add_comment_to_text_file(filepath, comment_text):
    """Add comment to text file."""
    try:
        # Read the current content
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if comment already exists at the beginning
        lines = content.split('\n')
        if lines and 'nutracia' in lines[0].lower():
            print(f"Comment already exists in: {filepath}")
            return True
        
        # Add comment at the beginning
        if content.strip():
            new_content = comment_text + '\n' + content
        else:
            new_content = comment_text + '\n'
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Added comment to: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def add_comment_to_binary_file(filepath, comment_text):
    """Add comment to binary file by appending metadata."""
    try:
        # For binary files, we'll append a small text comment at the end
        # This won't break the file but will update the modification time
        with open(filepath, 'ab') as f:
            metadata = f"\n# {comment_text} - {datetime.now().isoformat()}\n".encode('utf-8')
            f.write(metadata)
        
        print(f"✅ Added metadata to binary file: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing binary file {filepath}: {e}")
        return False

def process_file(filepath):
    """Process a single file to add the nutracia comment."""
    file_type = get_file_type(filepath)
    comment_text = get_comment_text(file_type)
    
    if file_type == 'binary':
        return add_comment_to_binary_file(filepath, comment_text)
    else:
        return add_comment_to_text_file(filepath, comment_text)

def main():
    """Main function to process all files in the repository."""
    repo_path = '/app/Hackunited1'
    
    # Get ALL files in the repository (including git files, but excluding certain git internals)
    all_files = []
    for root, dirs, files in os.walk(repo_path):
        # Skip some git internal directories that shouldn't be modified
        if 'objects' in root or 'logs' in root or 'refs' in root:
            continue
            
        for file in files:
            filepath = os.path.join(root, file)
            all_files.append(filepath)
    
    # Sort files for consistent processing
    all_files.sort()
    
    print(f"Found {len(all_files)} files to process")
    print("=" * 80)
    
    # Process each file
    success_count = 0
    failed_count = 0
    
    for filepath in all_files:
        relative_path = filepath.replace(repo_path + '/', '')
        print(f"Processing: {relative_path}")
        
        if process_file(filepath):
            success_count += 1
        else:
            failed_count += 1
    
    print("=" * 80)
    print(f"SUMMARY:")
    print(f"✅ Successfully processed files: {success_count}")
    print(f"❌ Failed to process files: {failed_count}")
    print(f"📊 Total files: {success_count + failed_count}")
    
    if failed_count == 0:
        print("\n🎉 SUCCESS: All files have been successfully modified with the 'nutracia' comment!")
    else:
        print(f"\n⚠️  WARNING: {failed_count} files could not be processed.")

if __name__ == '__main__':
    main()