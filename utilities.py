import re

def clean_text(text): 
     pattern = r'["\'{}]'
     return re.sub(pattern, '', text)