#include <wx/wx.h>
#include <wx/wxhtml.h>
#include <wx/htmllbox.h>

#include "data.h"
#include "fuzzysearch.h"

#include <vector>
#include <string>
#include <sstream>

using std::string;
using std::vector;



class MainFrame : public wxFrame {
public:
  MainFrame();
private:
  wxBoxSizer* v_sizer;
  wxBoxSizer* h_sizer;

  wxTextCtrl* input;
  wxSimpleHtmlListBox*  selection;
  wxHtmlWindow* description;

  void createComponents();
  void createLayout();
  void createBehavior();
};

class Application : public wxApp {
  bool OnInit() override ;
};


string colorIndexes(string str,vector<int> indexes);
