#pragma once

#include <string>

std::string concat(
    const char *title,
    const char *description,
    const char **posts,
    size_t n_posts);

std::string preprocess_en(std::string &text);
std::string preprocess_ru(std::string &text);

void postprocess_predictions(
    double *predictions, double *category_probabilities, size_t category_count, double threshold);
