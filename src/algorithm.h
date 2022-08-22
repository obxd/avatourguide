#ifndef ALGORITHM_H
#define ALGORITHM_H

#include <iostream>
#include <vector>
#include <array>
#include <algorithm>
#include <queue>
#include <tuple>

#include "data.h"
#include "levenshtein.h"

using std::string_view;
using std::vector;
using std::array;
using std::string;
using std::tuple;
using std::priority_queue;

vector<tuple< string, string, vector<int>>> fuzzysearch (const string_view input, const int maxRes);

#endif
