#include "fuzzysearch.h"

namespace fuzzysearch{

vector<IndexedMatch> fuzzysearch(string input, vector<string>& itemList, int maxRes){

  priority_queue<IndexedMatch> matches{};
  for (int i=0; i<itemList.size(); ++i)
  {
    matches.push(std::move(IndexedMatch(input, itemList[i], i)));
  }

  vector<IndexedMatch> res;
  for(int i=0; i<maxRes; ++i)
  {
    res.emplace_back(matches.top());
    matches.pop();
  }
  return res;

}
};
