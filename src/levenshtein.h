#ifndef LEVENSHTEIN_H
#define LEVENSHTEIN_H

#include <iostream>
#include <algorithm>
#include <vector>

using std::string_view;
using std::min;
using std::vector;

namespace LevenshteinDistance{

class LD
{
public:
  LD(string_view s, string_view t);

  /* return the Levenshtein distance btween the strings s and t */ 
  const int get_distance();

  /* return the Levenshtein ratio (LR), which creates a similarity ratio based on the LD.
   * btween the strings s and t */ 
  const double get_ratio();
  
  /* Reconstructing the edits of the input strings, storing indexes of t where there is 
   * a matches of chars from s to t
   * storing into matches vector */
  vector<int> get_target_matches();

private:
  const string_view s;
  const string_view t; 
  std::vector<std::vector<int> > d;  
  bool distance_calculated;

};

};

#endif // LEVENSHTEIN_H
