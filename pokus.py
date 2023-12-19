import os
import json

text_file_name = 'large_P_Hanes_Apologetika_03 Apologetika(VnC).txt'

with open(os.path.join('./text', text_file_name), 'r') as f:
    print(json.load(f))