import pandas as pd

df = pd.read_csv("data_es/test_rule_based_re_dataset.csv")
df.columns = ["doc_id", "text", "rml_s", "rml_e", "tst_s", "tst_e"]

def find_comma_not_decimal(s):
    for i, char in enumerate(s):
        if char == ",":
            before = s[i - 1] if i - 1 >= 0 else None
            after = s[i + 1] if i + 1 < len(s) else None
            
            if not (before.isdigit() and after.isdigit()):
                return True
                
    return False



def classify_relation(text):
    
    indexes = [text.find("[RML]"), text.find("[TST]")]
    indexes.sort()
    return not find_comma_not_decimal(text[indexes[0]: indexes[1]])

preds = df.text.apply(classify_relation)

print(preds)