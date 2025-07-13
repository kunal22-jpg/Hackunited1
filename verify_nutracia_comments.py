#!/usr/bin/env python3
"""
Verification script to confirm all files have the nutracia comment added.
"""

import os

def main():
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
    
    all_files.sort()
    
    print("VERIFICATION REPORT: Files with 'nutracia' comment added")
    print("=" * 80)
    
    success_count = 0
    failed_count = 0
    
    for filepath in all_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_line = f.readline().strip()
                
            if 'nutracia' in first_line.lower():
                relative_path = filepath.replace('/app/Hackunited1/', '')
                print(f"✅ {relative_path}")
                success_count += 1
            else:
                relative_path = filepath.replace('/app/Hackunited1/', '')
                print(f"❌ {relative_path} - Missing comment")
                failed_count += 1
                
        except Exception as e:
            relative_path = filepath.replace('/app/Hackunited1/', '')
            print(f"❌ {relative_path} - Error: {e}")
            failed_count += 1
    
    print("=" * 80)
    print(f"SUMMARY:")
    print(f"✅ Files with 'nutracia' comment: {success_count}")
    print(f"❌ Files without 'nutracia' comment: {failed_count}")
    print(f"📊 Total files processed: {success_count + failed_count}")
    
    if failed_count == 0:
        print("\n🎉 SUCCESS: All files have been successfully modified with the 'nutracia' comment!")
    else:
        print(f"\n⚠️  WARNING: {failed_count} files still need the comment added.")

if __name__ == '__main__':
    main()