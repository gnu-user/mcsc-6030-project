###############################################################################
#
# Plots the results from the matrix multiplication benchmarking.
# 
# Copyright (C) 2015, Jonathan Gillett
# All rights reserved.
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
library(stringr)
library(data.table)
library(psych)
library(ggplot2)
library(RColorBrewer)

figure_dir <- "./plots/"


# Parse the results
results <- data.table(results)




# Plot the assorted bool results, X is dims, Y is time, colour is benchmark
p <- ggplot(results, aes(x=dims, y=assorted_bool, colour=as.factor(benchmarks)))
p <- p + geom_line(size=1.5) + 
    scale_colour_manual(values = c(brewer.pal(3, "Set2"))) +
    labs(x = "Dimensions", y = "Time (Seconds)", 
         title = "Execution Time - Assorted Boolean Test",
         colour = "Benchmark")

file <- "assorted_bool.png"
file <- paste(figure_dir, file, sep="/")
ggsave(filename=file, plot=p, width=12, height=6)




# Plot the assorted int results, X is dims, Y is time, colour is benchmark
p <- ggplot(results, aes(x=dims, y=assorted_int, colour=as.factor(benchmarks)))
p <- p + geom_line(size=1.5) + 
    scale_colour_manual(values = c(brewer.pal(3, "Set2"))) +
    labs(x = "Dimensions", y = "Time (Seconds)", 
         title = "Execution Time - Assorted Integer Test",
         colour = "Benchmark")

file <- "assorted_int.png"
file <- paste(figure_dir, file, sep="/")
ggsave(filename=file, plot=p, width=12, height=6)




# Plot the assorted float results, X is dims, Y is time, colour is benchmark
p <- ggplot(results, aes(x=dims, y=assorted_float, colour=as.factor(benchmarks)))
p <- p + geom_line(size=1.5) + 
    scale_colour_manual(values = c(brewer.pal(3, "Set2"))) +
    labs(x = "Dimensions", y = "Time (Seconds)", 
         title = "Execution Time - Assorted Float Test",
         colour = "Benchmark")

file <- "assorted_float.png"
file <- paste(figure_dir, file, sep="/")
ggsave(filename=file, plot=p, width=12, height=6)




# Plot the adjacency matrix results, X is dims, Y is time, colour is benchmark
p <- ggplot(results, aes(x=dims, y=adjacency, colour=as.factor(benchmarks)))
p <- p + geom_line(size=1.5) + 
    scale_colour_manual(values = c(brewer.pal(3, "Set2"))) +
    labs(x = "Dimensions", y = "Time (Seconds)", 
         title = "Execution Time - Adjacency Matrix Test",
         colour = "Benchmark")

file <- "adjacency.png"
file <- paste(figure_dir, file, sep="/")
ggsave(filename=file, plot=p, width=12, height=6)




# Plot the stochastic results, X is dims, Y is time, colour is benchmark
p <- ggplot(results, aes(x=dims, y=stochastic, colour=as.factor(benchmarks)))
p <- p + geom_line(size=1.5) + 
    scale_colour_manual(values = c(brewer.pal(3, "Set2"))) +
    labs(x = "Dimensions", y = "Time (Seconds)", 
         title = "Execution Time - Stochastic Test",
         colour = "Benchmark")

file <- "stochastic.png"
file <- paste(figure_dir, file, sep="/")
ggsave(filename=file, plot=p, width=12, height=6)
