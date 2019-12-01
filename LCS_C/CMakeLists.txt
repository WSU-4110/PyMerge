cmake_minimum_required(VERSION 3.15)
project(LCS C)

set(CMAKE_C_STANDARD 99)

add_executable(LCS main.c myers_lcs.c myers_lcs.h xml_writer.c xml_writer.h)