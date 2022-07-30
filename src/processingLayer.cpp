#include "processingLayer.h"


pair<vector<string>, vector<void*> >process(string& input_text)
{
  pair<vector<string>, vector<void*> > resoult;

  if(input_text.length() >= 2) // strat searching after 2 chars
  {
    auto res = fuzzysearch(input_text, maps, 20);
    for (auto match: res)
    {
      string s = colorIndexes(match.get_target(), match.get_matches());
      string& d = desc[match.get_index()];
      resoult.first.emplace_back(s);
      resoult.second.emplace_back(static_cast<void*>(&d));
    }
  }

  return resoult;
}


stringstream& add_tags(stringstream& ss)
{
  stringstream temp;
  temp << "<span style='color:red;'>";
  temp << "<b>";
  temp << ss.rdbuf();
  ss = std::move(temp);
  ss << "</b>";
  ss << "</span>";
  return ss;
}


string colorIndexes(string str,vector<int> indexes)
{
  std::sort(indexes.begin(),indexes.end());

  int count = 0; // counting number of new charcters
  for(auto& index : indexes)
  {
    stringstream ss;
    ss << str[index + count];
    const string replacment = add_tags(ss).str();
    str.replace(index + count, 1, replacment);
    count += replacment.length() - 1;
  }

  return str;
}
