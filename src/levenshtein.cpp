#include "levenshtein.h"

namespace LevenshteinDistance{

LD::LD(string s, string t)
:s{s}, t{t}, distance_calculated{false}
{
  int n = s.length();
  int m = t.length();
  d =  vector<std::vector<int> >(n + 1, std::vector<int>(m + 1));
}

const int LD::get_distance()
{
  int n = s.length();
  int m = t.length();
  
  if (distance_calculated) return d[n][m];

  if (n == 0) 
    return m;
  
  if (m == 0) 
    return n;
  
  for (int i = 0; i < n + 1; ++i)
    d[i][0] = i;
  
  for (int j = 0; j < m + 1; ++j)
    d[0][j] = j;
  
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
      int cost = (t[j-1] == s[i-1]) ? 0 : 1;
      d[i][j] = min({
           d[i-1][j] + 1    // deletion
          ,d[i][j-1] + 1    // insertion
          ,d[i-1][j-1] + cost  // substitution
          });
    }
  }
  distance_calculated = true;
  return d[n][m];
}


const double LD::get_ratio()
{
  int n = s.length();
  int m = t.length();
  int distance;

  if(distance_calculated) 
    distance = d[n][m];
  else
    distance = get_distance();
  
  if(n == 0 && m == 0 ) return 0;
  
  return static_cast<double>((n + m - distance))/(n + m);
}


void LD::get_target_matches(vector<int>& matches)
{
  if(!distance_calculated) get_distance();

  int n = s.length();
  int m = t.length();

  while(n > 0 && m > 0)
  {
    int smallest = min({ d[n-1][m]
                        ,d[n][m-1]
                        ,d[n-1][m-1]});

    if(d[n][m] == smallest) // match
    {
        matches.push_back(m-1);
        --m;
        --n;
    }
    else if(d[n-1][m-1] == smallest) // substitusion
    {
        --n;
        --m;
    }
    else if(d[n-1][m] == smallest) // deletion
    {
        --n;
    }
    else if(d[n][m-1] == smallest) // insertion
    {
        --m;
    }
    else
    {
        throw std::runtime_error("bad d matrix");
    }
  }
}

};
