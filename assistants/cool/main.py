import os
from embedchain import Pipeline as App

os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"
os.environ["HF_HUB_CACHE"] = "/home/shaun/.cache/huggingface/hub"
os.environ["PYTORCH_PRETRAINED_BERT_CACHE"] = "/home/shaun/.cache/torch/transformers"
#os.environ["OPENAI_API_KEY"] = "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"

app = App.from_config(yaml_path="config.yaml")
app.add("https://www.forbes.com/profile/elon-musk", data_type='web_page')
app.add("https://en.wikipedia.org/wiki/Elon_Musk", data_type='web_page')
app.query("What is the net worth of Elon Musk today?")
# Answer: The net worth of Elon Musk today is $258.7 billion.

# app.add("@channel_name", data_type="youtube_channel")
# app.add('/path/to/file.pdf', data_type='pdf_file')
# Another eample:
#app.add('https://arxiv.org/pdf/1706.03762.pdf', data_type='pdf_file')
#app.query("What is the paper 'attention is all you need' about?", citations=True)