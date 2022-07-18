#include "MainWindow.h"

// Constructor for main window
MainWindow::MainWindow(QWidget *parent)
  :QWidget(parent)
{
  line_ = new QLineEdit();
  textBrowser_ = new QTextBrowser();
  list_ = new QListWidget();

  QGridLayout *mainLayout = new QGridLayout;
  mainLayout->addWidget(line_,0,0);
  mainLayout->addWidget(list_,1,0);
  mainLayout->addWidget(textBrowser_,1,1);

  setLayout(mainLayout);
  setWindowTitle(tr("avatourguide"));
  connect(line_, SIGNAL(textChanged(const QString &)), this, SLOT(onTextEnter(const QString &)));
  connect(list_, SIGNAL(itemSelectionChanged()), this, SLOT(onSelection()));
}


// Destructor
MainWindow::~MainWindow()
{
  delete line_;
  delete textBrowser_;
  delete list_;
}


void MainWindow::onTextEnter(const QString & text)
{
  // clear the items in the list and start the process
  list_->clear();
  // clear the description
  textBrowser_->clear(); 

  std::string input = text.toStdString();
  if(input.length() >= 2) // strat searching after 2 chars
  {
    auto res = fuzzysearch::fuzzysearch(input, maps, 20);
    for (auto match: res)
    {

      QListWidgetItem *item = new QListWidgetItem;
      QLabel* label = new QLabel{list_};

      QString qs = colorIndexes(match.get_target(), match.get_matches());
      label->setText(qs);

      QVariant index{match.get_index()};
      item->setData(Qt::UserRole, index);

      list_->addItem(item);
      list_->setItemWidget(item,label);
    }
    list_->setCurrentRow(0);
  }
}


void MainWindow::onSelection() // Handler for selection
{
  QListWidgetItem* currentItem = list_->currentItem();
  if (currentItem != 0)
  {
    QVariant data = currentItem->data(Qt::UserRole);
    int index = data.toInt();
    textBrowser_->clear(); 
    textBrowser_->append(desc[index]);
  }
}


QString colorIndexes(string str,vector<int> indexes)
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
  return QString::fromStdString(ss.str());
}
