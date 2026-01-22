import os
import re

def update_fonts():
    directory = r"c:\Users\Shalani A\Documents\Shalan\client projects\software company"
    
    # Update style.css first
    css_path = os.path.join(directory, "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add font variable to :root if not present
        if "--font-main" not in content:
            # Look for where to insert the variable in :root
            root_match = re.search(r':root\s*\{(.*?)\}', content, re.DOTALL)
            if root_match:
                root_content = root_match.group(1)
                new_root_content = root_content + "\n    --font-main: 'Inter', system-ui, -apple-system, sans-serif;"
                content = content.replace(root_content, new_root_content)
        
        # Update body font-family properly
        # Find the body selector and update its font-family
        body_match = re.search(r'body\s*\{(.*?)\}', content, re.DOTALL)
        if body_match:
            body_props = body_match.group(1)
            new_body_props = re.sub(r'font-family:\s*[^;]+;', "font-family: var(--font-main);", body_props)
            content = content.replace(body_props, new_body_props)
        else:
            # Fallback regex if body simple search fails
            content = re.sub(r"font-family: [^;]+;", "font-family: var(--font-main);", content)
        
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {css_path}")

    # Update all HTML files
    new_font_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
    
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Use DOTALL to match links spread over multiple lines
            font_links = re.findall(r'<link [^>]*fonts\.googleapis\.com[^>]*>', content, re.DOTALL)
            if font_links:
                first_link = font_links[0]
                content = content.replace(first_link, new_font_link)
                for other_link in font_links[1:]:
                    content = content.replace(other_link, "")
                
                # Cleanup any double newlines or formatting issues after removal
                # Also handle whitespace around the new link
                content = re.sub(r'\n\s*\n\s*', '\n\n', content)
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {filename}")
            else:
                # If no fonts.googleapis.com link found, maybe it's just missing? 
                # Let's check if it has a head tag and insert if missing Inter
                if "fonts.googleapis.com" not in content and "<head>" in content and "Inter" not in content:
                    content = content.replace("<head>", f"<head>\n    {new_font_link}")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Inserted font link in {filename}")

if __name__ == "__main__":
    update_fonts()
