cmake_minimum_required(VERSION 3.16)

project(AvalonianTourguide VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)
qt_standard_project_setup()

add_executable(avatourguide 
    data.cpp
    data.h
    fuzzysearch.cpp
    fuzzysearch.h
    levenshtein.cpp
    levenshtein.h
    main.cpp
    MainWindow.cpp
    MainWindow.h
    match.cpp
    match.h
)

target_link_libraries(avatourguide PRIVATE Qt6::Widgets)

set_target_properties(avatourguide PROPERTIES
    WIN32_EXECUTABLE ON
    MACOSX_BUNDLE ON
)

