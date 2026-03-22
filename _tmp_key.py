with open(r'C:\Users\itach\.openclaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Find viviai section
idx = content.find('viviai')
section = content[idx:idx+300]
print("VIVIAI SECTION:")
print(section)
print()

# Find vectorengine provider section
idx2 = content.find('api.vectorengine')
if idx2 > 0:
    section2 = content[idx2-50:idx2+300]
    print("VECTORENGINE SECTION:")
    print(section2)
