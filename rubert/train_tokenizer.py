from pathlib import Path

from transformers import BertTokenizer, AutoTokenizer

from tokenizers import Tokenizer
from tokenizers.models import WordPiece

# from tokenizers import ByteLevelBPETokenizer

# paths = [str(x) for x in Path("./eo_data/").glob("**/*.txt")]

# Initialize a tokenizer
# tokenizer = ByteLevelBPETokenizer()

# # Customize training
# tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
#     "<s>",
#     "<pad>",
#     "</s>",
#     "<unk>",
#     "<mask>",
# ])


# # Save files to disk
# tokenizer.save_model(".", "esperberto")

# tokenizer = AutoTokenizer.from_pretrained("prajjwal1/bert-small")
tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
# tokenizer = BertTokenizer()
print(dir(tokenizer))
print(tokenizer.vocab_files_names)


# print(tokenizer.vocab)
