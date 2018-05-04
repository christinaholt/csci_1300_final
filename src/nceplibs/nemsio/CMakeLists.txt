#------------------------------------------------------------------------------
#
project(nemsio)

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
# Look for packages
find_package(MPI)

#------------------------------------------------------------------------------
# Set the sources
set(SOURCES
	nemsio_module.f90
	nemsio_openclose.f90
	nemsio_read.f90
	nemsio_write.f90
)

if (MPI_Fortran_FOUND)
	list(APPEND SOURCES nemsio_module_mpi.f90)
endif(MPI_Fortran_FOUND)

#------------------------------------------------------------------------------
# Create a libraray
add_library(nemsio ${SOURCES})
target_link_libraries(nemsio LINK_PUBLIC)
#set_target_properties(nemsio PROPERTIES VERSION ${PROJECT_VERSION}
#SOVERSION ${PROJECT_VERSION_MAJOR})

if (MPI_Fortran_FOUND)
	include_directories(${MPI_Fortran_INCLUDE_PATH})
	target_link_libraries(nemsio ${MPI_Fortran_LIBRARIES})
endif(MPI_Fortran_FOUND)

#------------------------------------------------------------------------------
# Installation
install(TARGETS nemsio
	ARCHIVE DESTINATION "lib")
install(FILES
	${PROJECT_BINARY_DIR}/nemsio_module.mod
	${PROJECT_BINARY_DIR}/nemsio_openclose.mod
	${PROJECT_BINARY_DIR}/nemsio_read.mod
	${PROJECT_BINARY_DIR}/nemsio_write.mod
	DESTINATION "include/nemsio")

if (MPI_Fortran_FOUND)
	install(FILES
		${PROJECT_BINARY_DIR}/nemsio_module_mpi.mod
		DESTINATION "include/nemsio")
endif(MPI_Fortran_FOUND)
