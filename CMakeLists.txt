cmake_minimum_required(VERSION 3.22)

project("Learning Game" CXX C)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "") # works

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug 
        CACHE STRING "Choose the type of build (Debug or Release)" FORCE)
endif()

configure_file(config.h.in config.h)

file(GLOB SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)

# copy resource dir into build dir
file(COPY ${PROJECT_SOURCE_DIR}/sprites DESTINATION .)

find_package(SFML
    COMPONENTS
        system window graphics network audio REQUIRED)

include_directories(${PROJECT_SOURCE_DIR}/inc)

add_executable(sfml-app-cli ${SRC_FILES})

target_include_directories(sfml-app-cli 
    PRIVATE "{PROJECT_BINARY_DIR}")
target_link_libraries(sfml-app-cli sfml-graphics sfml-window sfml-system)


