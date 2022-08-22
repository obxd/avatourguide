#ifndef GUI_H
#define GUI_H

#include <wx/wx.h>
#include <wx/wxhtml.h>
#include <wx/htmllbox.h>

#include <string>

#include "processingLayer.h"

using std::string;


class MainFrame : public wxFrame {
public:
  MainFrame();
private:
  wxArrayString mnames;
  vector<string> mdesc;

  wxBoxSizer* v_sizer;
  wxBoxSizer* h_sizer;

  wxTextCtrl* input;
  wxSimpleHtmlListBox* selection;
  wxHtmlWindow* description;

  void createComponents();
  void createLayout();
  void createBehavior();
};

class Application : public wxApp {
  bool OnInit() override ;
};

#endif
