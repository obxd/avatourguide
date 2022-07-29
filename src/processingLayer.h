#ifndef PROCESSINGLAYER_H
#define PROCESSINGLAYER_H

#include <vector>
#include <string>
#include <sstream>
#include <utility>

#include "algorithm.h"
#include "data.h"

using std::string;
using std::vector;
using std::pair;
using std::stringstream;


vector<pair<string, string*> > process(string& input_text);


string colorIndexes(string str,vector<int> indexes);


stringstream& add_tags(stringstream& ss);

#endif
