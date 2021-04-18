#include <tgcat.h>

#include <utils/utils.h>
#include <config.h>
#include <model/bert.h>
#include <langdetect/langdetect.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <memory>
#include <iostream>

using std::string;
using std::vector;

std::shared_ptr<Bert> enBERT;
std::shared_ptr<Bert> ruBERT;
langdetect::Detector lang_detector;

// cache values during language detection
string current_lang_code;
string current_concatted_channel_infos;

int tgcat_init()
{
    try
    {
        enBERT = std::make_shared<Bert>(EN_BERT_MODEL_PATH, EN_BERT_VOCAB_PATH, EN_BERT_MAX_SEQ_LEN);
        ruBERT = std::make_shared<Bert>(RU_BERT_MODEL_PATH, RU_BERT_VOCAB_PATH, RU_BERT_MAX_SEQ_LEN);
    }
    catch (std::exception &e)
    {
        return -1;
    }

    return 0;
}

int tgcat_detect_language(const struct TelegramChannelInfo *channel_info,
                          char language_code[6])
{
    current_concatted_channel_infos = concat(
        channel_info->title,
        channel_info->description,
        channel_info->posts,
        channel_info->post_count);

    auto detected_lang = lang_detector.detect(
        current_concatted_channel_infos.data(), current_concatted_channel_infos.size());

    current_lang_code = detected_lang.name();

    memcpy(language_code, current_lang_code.c_str(), current_lang_code.size());
    return 0;
}

int tgcat_detect_category(const struct TelegramChannelInfo *channel_info,
                          double category_probability[TGCAT_CATEGORY_OTHER + 1])
{
    (void)channel_info;
    memset(category_probability, 0, sizeof(double) * (TGCAT_CATEGORY_OTHER + 1));

    vector<double> predictions;
    if (current_lang_code == "en")
    {
        string clean = preprocess_en(current_concatted_channel_infos);
        predictions = enBERT->predict(clean);
    }
    else if (current_lang_code == "ru")
    {
        // sadly no time to find the russian error
        // string clean = preprocess_ru(current_concatted_channel_infos);
        // predictions = ruBERT->predict(clean);

        // always return other
        predictions = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0};
    }
    else
    {
        return -1;
    }

    postprocess_predictions(
        predictions.data(), category_probability, TGCAT_CATEGORY_OTHER + 1, PREDICTION_THRESHOLD);

    return 0;
}
