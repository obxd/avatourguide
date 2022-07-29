#include "gui.h"

wxIMPLEMENT_APP(Application);


bool Application::OnInit() {
  auto frame = new MainFrame();
  frame->Show();
  return true;
}


MainFrame::MainFrame() : wxFrame(nullptr, wxID_ANY, "avatourguide")
{
  createComponents();
  createLayout();
  createBehavior();
}



void MainFrame::createComponents()
{
  // input text area
  input = new wxTextCtrl(this,wxID_ANY);

  // selection list
  selection = new wxSimpleHtmlListBox(this,wxID_ANY);
  selection->SetOwnBackgroundColour(wxColour(255,255,255));

  // description pane
  description = new wxHtmlWindow(this,wxID_ANY, wxDefaultPosition, wxDefaultSize, wxHW_SCROLLBAR_NEVER, "htmlWindow");
}



void MainFrame::createLayout()
{
  // sizer from top / buttom
  v_sizer= new wxBoxSizer(wxVERTICAL);

  // add input to the top
  v_sizer->Add(input, 0,wxEXPAND | wxALL, 10);

  // add horizonatl sizer to the bottom
  h_sizer = new wxBoxSizer(wxHORIZONTAL);
  v_sizer->Add(h_sizer, 1,wxEXPAND | wxALL, 10);

  // add selection list description to horizonatl sizer
  h_sizer->Add(selection, 1, wxEXPAND | wxALL, 10);
  h_sizer->Add(description, 1, wxEXPAND | wxALL, 10);

  this->SetSizerAndFit(v_sizer);
  v_sizer->Layout();
}



void MainFrame::createBehavior()
{
  // on text enter
  input->Bind(wxEVT_TEXT, [&](wxCommandEvent& event) {

      selection->Clear();
      std::string text = input->GetValue().ToStdString();

      if(text.length() >= 2) // strat searching after 2 chars
      {
        auto res = fuzzysearch::fuzzysearch(text, maps, 20);
        for (auto match: res)
        {
          string s = colorIndexes(match.get_target(), match.get_matches());
          string& d = desc[match.get_index()];
          selection->Append(s, (void *)&d);
        }
        selection->SetSelection(0);
      }
      wxPostEvent(selection, wxCommandEvent(wxEVT_LISTBOX));
      event.Skip();
  });

  // on selection
  selection->Bind(wxEVT_LISTBOX, [&](wxCommandEvent& event) {
      if(selection->GetSelection() != wxNOT_FOUND)
      {
        std::string* d = (std::string*) selection->GetClientData(selection->GetSelection());
        description->SetPage(*d);
      }
      else
      {
        description->SetPage("");
      }
      event.Skip();
  });
}

string colorIndexes(string str,vector<int> indexes)
{
  std::stringstream ss;
  std::sort(indexes.begin(),indexes.end());
  
  int j=0;
  for(int i=0; i<str.length(); ++i)
  {
    if(j<indexes.size() && indexes[j] == i )
    {
      if(str[indexes[j]] == ' ')
        ss << ' ';
      else
        ss << "<span style='color:red;'><b>" << str[indexes[j]] << "</b></span>";
      ++j;
    }
    else
    {
      ss << str[i];
    }
  }
  return ss.str();
}
