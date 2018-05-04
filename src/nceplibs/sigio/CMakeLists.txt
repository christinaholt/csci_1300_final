#------------------------------------------------------------------------------
#
project(sigio)
set(VERSION 1.0.0)

#------------------------------------------------------------------------------
cmake_minimum_required(VERSION 2.8)

#------------------------------------------------------------------------------
# Enable Fortran
enable_language(Fortran)

#------------------------------------------------------------------------------
# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to 'Release' as none was specified.")
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)

    # Set the possible values of build type for cmake-gui
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
                 "MinSizeRel" "RelWithDebInfo")
endif()

#------------------------------------------------------------------------------
# Set the sources
set(SOURCES
    sigio_module.f90
    sigio_r_module.f90
)

#------------------------------------------------------------------------------
# Create a libraray
add_library(sigio ${SOURCES})
target_link_libraries(sigio LINK_PUBLIC)

#------------------------------------------------------------------------------
# Installation
install(TARGETS sigio EXPORT sigio-targets
	ARCHIVE DESTINATION "lib")
install(FILES
	${PROJECT_BINARY_DIR}/sigio_module.mod
	${PROJECT_BINARY_DIR}/sigio_r_module.mod
	DESTINATION "include/sigio")

#------------------------------------------------------------------------------
# CMake package configuration
install(EXPORT sigio-targets
	DESTINATION "lib/cmake")
install(FILES sigio-config.cmake
	DESTINATION "lib/cmake")

