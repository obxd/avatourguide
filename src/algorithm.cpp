#include "algorithm.h"

vector<tuple< string, string, vector<int>>> fuzzysearch (const string_view input, const int maxRes)
{
  constexpr auto cmp{[](
        tuple <const MapData*, double, vector<int> >& a,
        tuple <const MapData*, double, vector<int> >& b ) {
    return get<1>(a) < get<1>(b);
  }};

  priority_queue<
      tuple <const MapData*, double ,vector<int>>,
      vector <tuple <const MapData*, double ,vector<int>>>,
      decltype(cmp)
    > pq {cmp};

  for(auto & item: Data)
  {
    auto ld = LevenshteinDistance::LD(input, item.name);
    double ratio = ld.get_ratio();
    vector<int> matches = ld.get_target_matches();

    tuple <
      const MapData*,
      double,
      vector<int>
    > itemScoreMatchs = std::make_tuple(&item , ratio, matches);

    pq.push(itemScoreMatchs);
  }


  vector<tuple<string, string, vector<int>>> res;
  for(int i=0; i<maxRes; ++i)
  {
    auto& item = pq.top();
    auto name = get<0>(item)->name;
    auto desc = get<0>(item)->description;
    auto matches = get<2>(item);
    res.emplace_back(std::make_tuple(name, desc, matches));
    pq.pop();
  }
  return res;

}
