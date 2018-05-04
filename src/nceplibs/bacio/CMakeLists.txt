#------------------------------------------------------------------------------
#
project(bacio)
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
        bacio.c
        baciof.f
        baciof.h
        bafrio.f
        byteswap.c
        chk_endianc.f
        clib.h
)

#------------------------------------------------------------------------------
# Create a libraray
add_library(bacio ${SOURCES})
target_link_libraries(bacio LINK_PUBLIC)

#------------------------------------------------------------------------------
# Add needed C flags
string(TOUPPER ${CMAKE_SYSTEM_NAME} UPPER_SYSTEM_NAME)
set(CMAKE_C_FLAGS ${CMAKE_C_FLAGS} "-D${UPPER_SYSTEM_NAME}")

#------------------------------------------------------------------------------
# Installation
install(TARGETS bacio EXPORT bacio-targets
	ARCHIVE DESTINATION "lib")
install(FILES ${PROJECT_BINARY_DIR}/bacio_module.mod
	DESTINATION "include/bacio")

#------------------------------------------------------------------------------
# CMake package configuration
install(EXPORT bacio-targets
	DESTINATION "lib/cmake")
install(FILES bacio-config.cmake
	DESTINATION "lib/cmake")

