#include <model/bert.h>

#include <exception>
#include <iostream>

using std::string;
using std::vector;

namespace t = torch;
namespace rd = radish;

Bert::Bert(const char *model_path, const char *vocab_path, int max_sequence_len)
{
    _max_sequence_len = max_sequence_len;

    try
    {
        _model = torch::jit::load(model_path);
        // TODO error throw
        _model.eval();
        _model.to(torch::kCPU);
    }
    catch (std::exception &e)
    {
        std::cerr << e.what();
        throw e;
    }

    bool success = _tokenizer.Init(vocab_path);
    if (!success)
    {
        auto msg = "Failed to load vocab file.\n";
        std::cerr << msg;
        throw std::runtime_error(msg);
    }
}

vector<double> Bert::predict(string &sinput)
{
    vector<t::jit::IValue> inputs = _make_inputs(sinput);
    auto output = _model.forward(inputs)
                      .toTuple()
                      ->elements()[0]
                      .toTensor();
    output = t::sigmoid(output);

    // something goes wrong here if we not copy the tensor before it is returned
    vector<double> predictions;
    predictions.reserve(42);

    auto data = output.accessor<float, 2>().data();
    for (int i = 0; i < 42; ++i)
        predictions.push_back(data[i]);

    return predictions;
}

vector<t::jit::IValue> Bert::_make_inputs(string &input_string)
{
    static t::Tensor whole_attention = t::full(_max_sequence_len, 1);
    // 0 token means "context", be classify => no second input_string => always 0
    static t::Tensor token_type_ids = t::full(_max_sequence_len, 0);

    // vector<int> attention; attention.reserve(max_sequence_len);
    // vector<int> token_type; token_type.reserve(max_sequence_len);

    // encoding will alter the original input_string
    vector<int> encoded_text = _tokenizer.Encode(input_string);

    t::Tensor attention_mask;

    encoded_text[0] = _tokenizer.ClsId();
    // no padding needed, prune the text
    if (encoded_text.size() >= _max_sequence_len)
    {
        encoded_text[_max_sequence_len - 1] = _tokenizer.SepId();
        attention_mask = whole_attention;
    }
    // pad text and attention mask
    else
    {
        encoded_text.reserve(_max_sequence_len);
        encoded_text.push_back(_tokenizer.SepId());
        attention_mask = whole_attention;

        // pad 0 until we reach max_sequence_len
        // fill the attention mask (0 where sequence is padded)
        for (int i = encoded_text.size(); i < encoded_text.capacity(); ++i)
        {
            encoded_text.push_back(0);
            attention_mask[i] = 0;
        }
    }

    auto options = t::TensorOptions().dtype(t::kInt32);
    auto input_ids = t::from_blob(encoded_text.data(), _max_sequence_len, options)
                         .to(t::kLong);

    return {
        input_ids.view({1, _max_sequence_len}),
        attention_mask.view({1, _max_sequence_len}),
        token_type_ids.view({1, _max_sequence_len}),
    };
}
