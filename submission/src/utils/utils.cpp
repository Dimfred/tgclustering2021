#include <utils/utils.h>

#include <iostream>
#include <algorithm>
#include <regex>

using std::string;

string concat(
    const char *title,
    const char *description,
    const char **posts,
    size_t n_posts)
{
    string concatted = title;
    concatted += " ";
    concatted += description;

    for (size_t post_idx = 0; post_idx < n_posts; ++post_idx)
    {
        concatted += " ";
        concatted += posts[post_idx];
    }

    return concatted;
}

void postprocess_predictions(
    double *predictions, double *category_probabilities, size_t category_count, double threshold)
{
    // sum all predictions > thresh, needed to normalize the percentage values
    double sum_probabilities = 0.0;
    for (size_t cat_idx = 0; cat_idx < category_count; ++cat_idx)
    {
        double cat_prediction = predictions[cat_idx];
        if (cat_prediction >= threshold)
            sum_probabilities += cat_prediction;
    }

    // threshold and normalize the predictions
    if (sum_probabilities != 0.0)
    {
        // normalize the category values and set the output vector
        for (size_t cat_idx = 0; cat_idx < category_count; ++cat_idx)
        {
            float cat_prediction = predictions[cat_idx];
            if (cat_prediction >= threshold)
                category_probabilities[cat_idx] = (double)(cat_prediction / sum_probabilities);
        }
    }
    // just assign other
    else
    {
        category_probabilities[category_count - 1] = 1.0;
    }
}

bool is_unicode(char c);
string strip_unicode(string &str);
string make_clean(const string& str);

string preprocess_en(string &text)
{
    auto clean = strip_unicode(text);
    clean = make_clean(clean);
    return clean;
}

string preprocess_ru(string& text)
{
    return text;
}

inline bool is_ascii(char c)
{
    return 0 <= c && c < 128;
}

string strip_unicode(string& str)
{
    string unicode_free;
    unicode_free.reserve(str.size());

    for (char c : str)
        if (is_ascii(c))
            unicode_free += c;

    return unicode_free;
}

string match_single_chars = R"(([\n|\r|\t|\||·|\[|\]|\(|\)|\"|”|,|“|\*|;|'|~]+))";
string match_at_least_two = R"(([\-|=|\s|:|\.|.|-|_|—][\-|=|\s|:|\.|.|-|_|—]+))";
string clean_expr = "(" + match_single_chars + "|" + match_at_least_two + ")";
std::regex clean_regex(clean_expr);

string match_two_spaces = R"(\s\s+)";
std::regex two_space_regex(match_two_spaces);

string make_clean(const string& str)
{
    auto clean = std::regex_replace(str, clean_regex, " ");
    clean = std::regex_replace(clean, two_space_regex, " ");
    return clean;
}
