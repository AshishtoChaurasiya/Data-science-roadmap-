import paralleldots
paralleldots.set_api_key('tw8BaXGEG1DPJiCZJSBxrS6o12FE83aWencrGg4a5CE')

def ner(text):
    ner = paralleldots.ner(text)
    return ner