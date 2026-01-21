import os
import re

directory = r'c:\Users\Shalani A\Documents\Shalan\client projects\software company'

img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
bg_pattern = re.compile(r'background-image:\s*url\([\'"]?([^\'"\)]+)[\'"]?\)', re.IGNORECASE)
alt_pattern = re.compile(r'alt=["\']([^"\']+)["\']', re.IGNORECASE)

print("--- Image Audit ---")
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"\nFile: {filename}")
        for i, line in enumerate(lines):
            # Check for img tags
            for match in img_pattern.finditer(line):
                src = match.group(1)
                # Find alt if present in the same tag match (simplified)
                # We need to look at the whole tag.
                tag = match.group(0)
                alt_match = alt_pattern.search(tag)
                alt = alt_match.group(1) if alt_match else "NO ALT"
                print(f"  Line {i+1} [IMG]: {src} (Alt: {alt})")
                
            # Check for background images
            for match in bg_pattern.finditer(line):
                url = match.group(1)
                print(f"  Line {i+1} [BG]: {url}")
