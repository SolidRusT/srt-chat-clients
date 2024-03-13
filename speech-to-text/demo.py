import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
sample = dataset[0]["audio"]

result = pipe(sample)
print(result["text"])

### Other options
## Input directly from mp3
# result = pipe("audio.mp3")
## Specify language
# result = pipe(sample, generate_kwargs={"language": "english"})
## Translate
# result = pipe(sample, generate_kwargs={"task": "translate"})
## Sentence level timestamps
# result = pipe(sample, return_timestamps=True)
# print(result["chunks"])
## Word level chunking
# result = pipe(sample, return_timestamps="word")
# print(result["chunks"])
## Combine methods
# result = pipe(sample, return_timestamps=True, generate_kwargs={"language": "french", "task": "translate"})
# print(result["chunks"])

## Setup flash attention
# pip install --upgrade pip
# pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate datasets[audio]
# pip install flash-attn --no-build-isolation

# model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True, use_flash_attention_2=True)


## Older or shit GPUs
# pip install --upgrade optimum
# model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
# + model = model.to_bettertransformer()

