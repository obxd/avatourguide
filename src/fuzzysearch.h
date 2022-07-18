#ifndef FUZZYSEARCH_H
#define FUZZYSEARCH_H

#include "match.h"
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using std::vector;
using std::priority_queue;

namespace fuzzysearch{

class IndexedMatch :public Matching::Match
{
public:
    IndexedMatch(string source, string target, int i)
      :index{i},Match{source,target}{};

    int get_index() const {return index;};
    
private:
    int index;
};

vector<IndexedMatch> fuzzysearch(string input, vector<string>& itemList, int maxRes);
}

#endif // FUZZYSEARCH_H
