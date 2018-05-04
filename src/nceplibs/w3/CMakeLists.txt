#------------------------------------------------------------------------------
#
project(w3)
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
# Find dependencies
if (CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    find_package(sigio REQUIRED)
else()
    include_directories(${CMAKE_CURRENT_BINARY_DIR}/../sigio)
    link_directories(${CMAKE_CURRENT_BINARY_DIR}/../sigio)
    set(SIGIO_LIBRARIES sigio)
endif()

#------------------------------------------------------------------------------
# Set the sources
set(SOURCES
	aea.f		getgbp.f	w3ai00.f	w3fi82.f
	errexit.f	getgi.f		w3ai01.f	w3fi83.f
	errmsg.f	getgir.f	w3ai08.f	w3fi88.f
	fparsei.f	gtbits.f	w3ai15.f	w3fi92.f
	fparser.f	idsdef.f	w3ai18.f	w3fp11.f
	gbyte.f		instrument.f	w3ai19.f	w3fp12.f
	gbytec.f	iw3jdn.f	w3ai24.f	w3fp13.f
	gbytes.f	iw3pds.f	w3ai38.f	w3fs13.f
	gbytesc.f	iw3unp29.f	w3ai39.f	w3fs15.f
	getbit.f	ixgb.f		w3aq15.f	w3fs21.f
	getgb.f		lengds.f	w3as00.f	w3fs26.f
	getgb1.f	makwmo.f	w3difdat.f	w3ft32.f
	getgb1r.f	mkfldsep.f	w3doxdat.f	w3kind.f
	getgb1re.f	mova2i.c	w3fi01.f	w3locdat.f
	getgb1s.f	pdsens.f	w3fi04.f	w3movdat.f
	getgbe.f	pdseup.f	w3fi58.f	w3nogds.f
	getgbeh.f	putgb.f		w3fi59.f	w3pradat.f
	getgbem.f	putgbe.f	w3fi62.f	w3reddat.f
	getgbemh.f	putgben.f	w3fi63.f	w3tagb.f
	getgbemn.f	putgbex.f	w3fi64.f	w3trnarg.f
	getgbemp.f	putgbn.f	w3fi68.f	w3unpk77.f
	getgbep.f	q9ie32.f	w3fi69.f	w3utcdat.f
	getgbex.f	r63w72.f	w3fi71.f	w3valdat.f
	getgbexm.f	sbyte.f		w3fi72.f	w3ymdh4.f
	getgbh.f	sbytec.f	w3fi73.f	xmovex.f
	getgbm.f	sbytes.f	w3fi74.f	xstore.f
	getgbmh.f	sbytesc.f	w3fi75.f
	getgbmp.f	skgb.f		w3fi76.f
)

set_source_files_properties(aea.f PROPERTIES COMPILE_FLAGS -fno-range-check)
set_source_files_properties(q9ie32.f PROPERTIES COMPILE_FLAGS -fno-range-check)
set_source_files_properties(w3ai00.f PROPERTIES COMPILE_FLAGS -fno-range-check)
set_source_files_properties(w3ai39.f PROPERTIES COMPILE_FLAGS -fno-range-check)

#------------------------------------------------------------------------------
# Create a libraray
add_library(w3 ${SOURCES})
target_link_libraries(w3 LINK_PUBLIC)

#------------------------------------------------------------------------------
# Add needed C flags
string(TOUPPER ${CMAKE_SYSTEM_NAME} UPPER_SYSTEM_NAME)
set(CMAKE_C_FLAGS ${CMAKE_C_FLAGS} "-D${UPPER_SYSTEM_NAME}")

#------------------------------------------------------------------------------
# Installation
install(TARGETS w3 EXPORT w3-targets
	ARCHIVE DESTINATION "lib")

#------------------------------------------------------------------------------
# CMake package configuration
install(EXPORT w3-targets
	DESTINATION "lib/cmake")
install(FILES w3-config.cmake
	DESTINATION "lib/cmake")

