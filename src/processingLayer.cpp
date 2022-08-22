#include "processingLayer.h"


pair< wxArrayString, vector< string>> process(const string_view& input_text)
{
  pair< wxArrayString, vector< string>> resoult;

  if(input_text.length() >= 2 && input_text.length() < 50) // strat searching after 2 chars and less than 50
  {
    auto res = fuzzysearch(input_text, 20);
    for (auto & item: res)
    {
      resoult.first.Add(wxString{colorIndexes(get<0>(item),get<2>(item))});
      resoult.second.emplace_back(get<1>(item));
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


string colorIndexes(string_view str,vector<int> indexes)
{
  std::string colored{str};
  std::sort(indexes.begin(),indexes.end());

  int count = 0; // counting number of new charcters
  for(auto& index : indexes)
  {
    stringstream ss;
    ss << colored[index + count];
    const std::string replacment = add_tags(ss).str();
    colored.replace(index + count, 1, replacment);
    count += replacment.length() - 1;
  }
  return colored;
}
