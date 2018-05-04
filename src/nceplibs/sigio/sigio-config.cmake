get_filename_component(SELF_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
include(${SELF_DIR}/sigio-targets.cmake)
get_filename_component(sigio_INCLUDE_DIRS "${SELF_DIR}/../../include/sigio" ABSOLUTE)

