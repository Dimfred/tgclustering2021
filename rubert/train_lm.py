# from trainer import Trainer

from transformers import Trainer
from transformers import AutoTokenizer, BertModel, BertConfig, BertForMaskedLM
from transformers import TrainingArguments
from transformers import DataCollatorForLanguageModeling

import torch as t

import corus as cor
from transformers.utils.dummy_pt_objects import AutoModel, LineByLineTextDataset

import utils
from config import config


class RuDataset(t.utils.data.Dataset):
    def __init__(self, tokenizer, eval=False):
        self.tokenizer = tokenizer
        self.fact_ru = [item.text for item in cor.load_factru(config.fact_ru)]

    def __len__(self):
        return len(self.fact_ru)

    def __getitem__(self, i):
        return self.tokenizer.encode_plus(
            self.fact_ru[i], max_length=512, truncation=True
        )


# for record in records:
#     print(record)
LineByLineTextDataset

tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased", max_len=512)
model_config = BertConfig.from_json_file("config.json")
model = BertForMaskedLM(model_config)
print(model.num_parameters())
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
        num_train_epochs=1,
        per_device_train_batch_size=1,
        save_steps=10_000,
        save_total_limit=30,
    ),
)
trainer.train()
trainer.save_model("./ruBERT")


model.cpu()
