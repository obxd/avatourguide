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
  selection->SetOwnBackgroundColour(wxColour(255,255,255)); // overide system background color

  // description pane
  description = new wxHtmlWindow(this,wxID_ANY, wxDefaultPosition, wxDefaultSize, wxHW_SCROLLBAR_NEVER, "htmlWindow");
}


void MainFrame::createLayout()
{
  // sizer from top / buttom
  v_sizer= new wxBoxSizer(wxVERTICAL);

  // add input to the top
  v_sizer->Add(input, 0, wxEXPAND | wxALL, 10);

  // add horizonatl sizer to the bottom
  h_sizer = new wxBoxSizer(wxHORIZONTAL);
  v_sizer->Add(h_sizer, 1, wxEXPAND | wxALL, 10);

  // add selection list and description to horizonatl sizer
  h_sizer->Add(selection, 1, wxEXPAND | wxALL, 10);
  h_sizer->Add(description, 1, wxEXPAND | wxALL, 10);

  this->SetSizer(v_sizer);
  v_sizer->Layout();
  this->SetSize(wxSize(800,600));
}


void MainFrame::createBehavior()
{
  // on text enter
  // -------------
  input->Bind(wxEVT_TEXT, [&](wxCommandEvent& event) {

      selection->Clear();
      string text = input->GetValue().ToStdString();

      for (auto& [name,data]: process(text))
        selection->Append(name, (void *)data);

      if(!selection->IsEmpty())
        selection->SetSelection(0);

      event.Skip();

      wxPostEvent(selection, wxCommandEvent(wxEVT_LISTBOX)); // emit selection changed event
  });

  // on selection
  // -------------
  selection->Bind(wxEVT_LISTBOX, [&](wxCommandEvent& event) {
      if(selection->GetSelection() != wxNOT_FOUND)
      {
        string* data = (string*) selection->GetClientData(selection->GetSelection());
        description->SetPage(*data);
      }
      else
      {
        description->SetPage("");
      }
      event.Skip();
  });
}

