#ifndef ALGORITHM_H
#define ALGORITHM_H

#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

#include "levenshtein.h"

using std::string;
using std::vector;
using std::priority_queue;


class Match{
public:
  Match(string source, string target);
  Match(const Match&) = default;
  Match(Match&&) = default;

  Match& operator=(const Match& other);
  Match& operator=(Match&& other);

  const string get_source() const;
  const string get_target() const;
  const vector<int> get_matches() const;
  const double get_score() const;

private:
  string source;
  string target;
  vector<int> matches; // on target
  double score;
};


bool operator<(const Match& lval, const Match& rval);


class IndexedMatch :public Match
{
public:
    IndexedMatch(string source, string target, int i)
      :index{i},Match{source,target}{};

    int get_index() const {return index;};
    
private:
    int index;
};


vector<IndexedMatch> fuzzysearch(string input, vector<string>& itemList, int maxRes);

#endif
