import os
import re

def update_fonts():
    directory = r"c:\Users\Shalani A\Documents\Shalan\client projects\software company"
    new_font_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
    
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Use DOTALL to match links spread over multiple lines
            # Be more aggressive: match any link tag containing fonts.googleapis.com
            pattern = re.compile(r'<link\s+[^>]*?href="https://fonts\.googleapis\.com/[^>]*?>', re.DOTALL)
            font_links = pattern.findall(content)
            
            if font_links:
                print(f"Found {len(font_links)} font links in {filename}")
                first_link = font_links[0]
                content = content.replace(first_link, new_font_link)
                for other_link in font_links[1:]:
                    content = content.replace(other_link, "")
                
                # Cleanup
                content = re.sub(r'\n\s*\n\s*', '\n\n', content)
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {filename}")
            else:
                # Try a broader search
                if "fonts.googleapis.com" in content:
                    print(f"DEBUG: Found 'fonts.googleapis.com' in {filename} but pattern didn't match.")
                    # Let's try to find any link tag with it
                    link_match = re.search(r'<link[^>]*?https://fonts\.googleapis\.com[^>]*?>', content, re.DOTALL)
                    if link_match:
                        link_text = link_match.group(0)
                        print(f"DEBUG: Found link text: {link_text[:50]}...")
                        content = content.replace(link_text, new_font_link)
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"Updated {filename} with fallback pattern")

if __name__ == "__main__":
    update_fonts()
