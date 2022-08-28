def read_pneumonia_data(name):
    import pandas as pd
    fp = "https://raw.githubusercontent.com/abchapman93/Melbourne_COMP90089_NLP/"\
    f"main/melbourne_comp90089_nlp/data/pneumonia_data_{name}.json"
    return pd.read_json(fp)
