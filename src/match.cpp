#include "match.h"

namespace Matching{

Match::Match(string source, string target)
:source{source},target{target},matches{},score{0}
{
  LevenshteinDistance::LD ld{source,target};
  score = ld.get_ratio();
  ld.get_target_matches(matches);
}

Match& Match::operator=(const Match& other) 
{
    matches = other.matches;
    score = other.score;
    source = other.source;
    target = other.target;
    return *this;
}

Match& Match::operator=(Match&& other)
{
    score   = other.score;
    source  = other.source;
    target  = other.target;
    matches = std::move(other.matches);

    other.score = 0;
    other.source = "";
    other.target = "";
    return *this;
}

const string Match::get_source() const
{
  return source;
}

const string Match::get_target() const
{
  return target;
}

const vector<int> Match::get_matches() const
{
  return matches;
}

const double Match::get_score() const
{
 return score;
}

bool operator<(const Match& lval, const Match& rval)
{
  return lval.get_score() < rval.get_score();
}

};
