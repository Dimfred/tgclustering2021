# from trainer import Trainer

from transformers import Trainer, pipeline
from transformers import AutoTokenizer, BertModel, BertConfig, BertForMaskedLM
from transformers import TrainingArguments
from transformers import DataCollatorForLanguageModeling


import torch as t

import corus as cor
from transformers.utils.dummy_pt_objects import AutoModel, LineByLineTextDataset

import utils
from config import config
import copy
import sys


def check():
    mname = "outputs/checkpoint-130000"
    fill_mask = pipeline(
        "fill-mask",
        model=mname,
        tokenizer=mname
    )

    #sentences = [item.text for item in cor.load_factru(config.fact_ru)]
    sentences = [
        "Доброе утро",
        "во время автогонки произошла авария"
    ]


    token = "[MASK]"
    for s in sentences:
        s = s.split(" ")
        
        for i in range(len(s)):
            ns = copy.deepcopy(s)
            ns[i] = token
            ns = " ".join(ns)

            print(ns)
            res = fill_mask(ns)
            print(res)
            input()
    
    sys.exit()

class RuDataset(t.utils.data.Dataset):
    def __init__(self, tokenizer, eval=False):
        self.tokenizer = tokenizer
        self.tokenizer_params = {
            "max_length": 128, 
            "truncation": True, 
            "add_special_tokens": True,
        }
        fact_ru = [item.text for item in cor.load_factru(config.fact_ru)]

        # TEST
        self.tokenizer.encode_plus(fact_ru[0], **self.tokenizer_params)

        lenta_ru = []
        lenta_ru = [item.text for item in cor.load_lenta(config.lenta_ru)]

        wiki_ru = []
        #wiki_ru = [item.text for item in cor.load_wiki(config.wiki_ru)]
        with open("data/ru/wiki.txt", "r") as f:
            wiki_ru = [l.strip() for l in f if len(l) > 35]

        self.data = fact_ru + wiki_ru + lenta_ru


    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.tokenizer.encode_plus(self.data[i], **self.tokenizer_params)




#check()

tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased", max_len=128)
model_config = BertConfig.from_json_file("config.json")
model = BertForMaskedLM(model_config)
#model = BertForMaskedLM.from_pretrained("outputs/checkpoint-15000")

dataset = RuDataset(tokenizer)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

trainer = Trainer(
    model,
    data_collator=data_collator,
    train_dataset=dataset,
    tokenizer=tokenizer,
    # prediction_loss_only=True,
    args=TrainingArguments(
        output_dir="outputs",
        overwrite_output_dir=True,
        num_train_epochs=5,
        per_device_train_batch_size=29,
        save_steps=5_000,
        save_total_limit=2,
        gradient_accumulation_steps=2
    ),
)
trainer.train()
trainer.save_model("./ruBERT")


model.cpu()
