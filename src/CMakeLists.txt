cmake_minimum_required(VERSION 3.16)

project(avatourguide VERSION 1.0.0 LANGUAGES CXX)

find_package(wxWidgets COMPONENTS html core base REQUIRED)
include(${wxWidgets_USE_FILE})

# Options
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Target
add_executable(avatourguide 
    data.cpp
    data.h
    levenshtein.cpp
    levenshtein.h
    algorithm.cpp
    algorithm.h
    gui.cpp
    gui.h
    processingLayer.h
    processingLayer.cpp
)

target_link_libraries(${PROJECT_NAME} 
  ${wxWidgets_LIBRARIES}
)

set_target_properties(${PROJECT_NAME} PROPERTIES
    WIN32_EXECUTABLE ON
    MACOSX_BUNDLE ON
)

