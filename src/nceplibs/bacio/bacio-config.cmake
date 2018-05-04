get_filename_component(SELF_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
include(${SELF_DIR}/bacio-targets.cmake)
get_filename_component(bacio_INCLUDE_DIRS "${SELF_DIR}/../../include/bacio" ABSOLUTE)

