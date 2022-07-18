#ifndef MATCH_H
#define MATCH_H

#include <vector>
#include <iostream>
#include "levenshtein.h"
using std::string;
using std::vector;

namespace Matching{

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

};
#endif // MATCH_H
