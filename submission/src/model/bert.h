#pragma once
#include <torch/script.h>
#include <radish/bert/bert_tokenizer.h>

#include <memory>
#include <string>

class Bert
{
public:
    Bert(const char *model_path, const char *vocab_path, int max_sequence_len);
    std::vector<double> predict(std::string &inputs);

private:
    std::vector<torch::jit::IValue> _make_inputs(std::string &input_string);

    torch::jit::script::Module _model;
    radish::BertTokenizer _tokenizer;
    int _max_sequence_len;
};
