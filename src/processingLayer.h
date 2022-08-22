#ifndef PROCESSINGLAYER_H
#define PROCESSINGLAYER_H

#include <vector>
#include <string>
#include <sstream>
#include <utility>

#include <wx/string.h>
#include <wx/arrstr.h>
#include <wx/clntdata.h>

#include "algorithm.h"
#include "data.h"

using std::string_view;
using std::string;
using std::vector;
using std::pair;
using std::stringstream;


/*
  * processing the input text 
  * returning a vector of 
  * map name and description pairs
  * the map name if formated with html tags to show the matches.
  */

pair< wxArrayString, vector< string>> process(const string_view& input_text);


string colorIndexes(string_view str,vector<int> indexes);


stringstream& add_tags(stringstream& ss);

#endif
