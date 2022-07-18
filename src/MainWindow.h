#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "data.h"
#include "fuzzysearch.h"

#include <vector>
#include <string>
#include <sstream>

#include <QWidget>
#include <QtWidgets>
#include <QLineEdit>
#include <QListWidget>
#include <QListWidgetItem>
#include <QTextBrowser>

using std::string;
using std::vector;

class MainWindow : public QWidget
{
  Q_OBJECT

  public:
  explicit MainWindow(QWidget *parent = 0); //Constructor
  ~MainWindow(); // Destructor
  
private slots:
  void onTextEnter(const QString &); // Handler for key presses
  void onSelection(); // Handler for selection

private:
  QLineEdit* line_;
  QListWidget* list_;
  QTextBrowser* textBrowser_;
};

QString colorIndexes(string str, vector<int> matches);

#endif // MAINWINDOW_H
