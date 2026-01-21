import os
import re

directory = r'c:\Users\Shalani A\Documents\Shalan\client projects\software company'

# Mapping Old IDs to New Unsplash Photo IDs (Premium Tech/Corporate)
id_map = {
    # System/Server
    '180': '1558494949-ef526b0042a0', # Servers
    # Cybersecurity
    '60': '1555949963-ff9fe0c870eb', # Code/Screen
    # BI / Analytics
    '20': '1551288049-bebda4e38f71', # Charts
    # Office / Hero
    '1': '1497366216548-37526070297c', # Modern Office (Hero)
    '3': '1522071820081-009f0129c71c', # Office Collaboration
    '201': '1519389950473-47ba0277781c', # Team Meeting (CTA)
    # Coding / Web
    '119': '1498050108023-c5249f4df085', # Code Laptop
    '199': '1517694712202-14dd9538aa97', # Mac code
    '2': '1531403009284-440f080d1e12', # Planning/Whiteboard
    '355': '1552664730-d307ca884978', # Team High Five/Launch
    # Mobile
    '129': '1512941937669-90a1b58e7e9c', # Holding Phone
    '111': '1555774698-4b791503597e', # Mobile Dev
    '145': '1551650975-87deedd944c3', # App mockup
    '250': '1512941937669-90a1b58e7e9c', # Phone BG
    # Cloud / Tech abstract
    '48': '1451187580459-43490279c0fa', # Cloud network
    '160': '1518770660439-4636190af475', # Chip/Tech
    # Design
    '3': '1581291518633-83b4ebd1d83e', # Wireframing (if used in UI context? ID 3 is reused)
    '29': '1586717791821-3f44a5638d0f', # UI Screen
    '6': '1509391364320-25aa37585b03', # Bulb/Thinking
    '39': '1581291518633-83b4ebd1d83e', # Prototype
    '445': '1561070791-2526d30994b5', # Gradient/Design BG
    '366': '1581291518633-83b4ebd1d83e', # Dashboard
    # AI
    '203': '1620712943543-0a3ac2774413', # AI Brain
    '403': '1451187580459-43490279c0fa', # Network Global
    # Projects
    '106': '1556742049-0cfed4f7a07d', # FinTech
    '96': '1576091160399-112ba8d25d1d', # Health
    '237': '1639762681485-074b7f938ba0', # Crypto
    '450': '1507238691740-187a5b1d37b8', # Planning
    # About Page Specifics (Timeline)
    '111': '1522202176988-66273c2fd55f', # Garage/Startup
    '180': '1542744173-8e7e53415bb0', # Growth/Meeting
    '403': '1522071901878-705333124cba', # Global Team
    # Default fallback
    'default': '1497366216548-37526070297c'
}

# Mapping people
people_map = [
    ('32.jpg', '1560250097-0b93528c311a'), # CEO
    ('44.jpg', '1573496359142-b8d87734a5a2'), # CTO
    ('86.jpg', '1472099645785-5658abf4ff4e'), # Lead Dev
    ('65.jpg', '1580489944761-15a19d654956'), # Designer
]

# Regex patterns
picsum_pattern = re.compile(r'https://picsum\.photos/id/(\d+)/(\d+)/(\d+)')
picsum_bg_pattern = re.compile(r'https://picsum\.photos/id/(\d+)/(\d+)/(\d+)')
randomuser_pattern = re.compile(r'https://randomuser\.me/api/portraits/(men|women)/(\d+)\.jpg')

def replace_picsum(match):
    pid = match.group(1)
    w = match.group(2)
    h = match.group(3)
    
    # Select unsplash ID
    unsplash_id = id_map.get(pid, id_map['default'])
    
    # Construct new URL
    return f'https://images.unsplash.com/photo-{unsplash_id}?auto=format&fit=crop&w={w}&h={h}&q=80'

def replace_user(match):
    uid = match.group(2) + ".jpg"
    
    # Find mapped ID
    new_id = people_map[0][1] # Default
    for old, new in people_map:
        if old == uid:
            new_id = new
            break
            
    return f'https://images.unsplash.com/photo-{new_id}?auto=format&fit=crop&w=400&h=400&q=80'

def process_files():
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace Picsum
            new_content = picsum_pattern.sub(replace_picsum, content)
            
            # Replace RandomUser
            new_content = randomuser_pattern.sub(replace_user, new_content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated images in {filename}")
                count += 1
            else:
                print(f"No changes in {filename}")

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    process_files()
