#include "processingLayer.h"


vector<pair<string, string*>>process(string& input_text)
{
  vector<pair<string, string*> > resoult;

  if(input_text.length() >= 2) // strat searching after 2 chars
  {
    auto res = fuzzysearch(input_text, maps, 20);
    for (auto match: res)
    {
      string s = colorIndexes(match.get_target(), match.get_matches());
      string& d = desc[match.get_index()];
      resoult.emplace_back(std::make_pair(s,&d));
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
