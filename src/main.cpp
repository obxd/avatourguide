#include "MainWindow.h"
#include <QApplication>
#include <iostream>

int main(int argc, char *argv[])
try {
  QApplication a(argc, argv);
  MainWindow w;
  w.show();
  return a.exec();
}
catch(std::exception& e) {
  std::cerr << e.what() << '\n';
  return 1;
}
catch(...) {
  std::cerr << "Something terrible happened!\n";
  return 2;
}
