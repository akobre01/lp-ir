#!/bin/bash

# Uniform scores
python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/affinity_500_900_6_3/assignments/20151025_211505622932-assignments.csv -m ./results/matching_exp/affinity_500_900_6_3/makespan/20151025_211505622932-makespan.csv
python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/relaxed_500_900_6_3/assignments/20151025_211505639276-assignments.csv -m ./results/matching_exp/relaxed_500_900_6_3/makespan/20151025_211505639276-makespan.csv
python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/complete-relax_500_900_6_3/assignments/20151025_211505634055-assignments.csv -m ./results/matching_exp/complete-relax_500_900_6_3/makespan/20151025_211505634055-makespan.csv
python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/makespan_500_900_6_3/assignments/20151025_211505627063-assignments.csv -m ./results/matching_exp/makespan_500_900_6_3/makespan/20151025_211505627063-makespan.csv

# Original Skill Based
python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/affinity_500_900_6_3/assignments/20151022_170140894619-assignments.csv -m ./results/matching_exp/affinity_500_900_6_3/makespan/20151022_170140894619-makespan.csv
python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/relaxed_500_900_6_3/assignments/20151022_170141072512-assignments.csv -m ./results/matching_exp/relaxed_500_900_6_3/makespan/20151022_170141072512-makespan.csv
python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/complete-relax_500_900_6_3/assignments/20151022_170140850093-assignments.csv -m ./results/matching_exp/complete-relax_500_900_6_3/makespan/20151022_170140850093-makespan.csv
python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/makespan_500_900_6_3/assignments/20151022_170140945548-assignments.csv -m ./results/matching_exp/makespan_500_900_6_3/makespan/20151022_170140945548-makespan.csv

# Integer scores
python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/affinity_500_900_6_3/assignments/20151028_003741291372-assignments.csv -m ./results/matching_exp/affinity_500_900_6_3/makespan/20151028_003741291372-makespan.csv
python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/relaxed_500_900_6_3/assignments/20151028_003741379816-assignments.csv -m ./results/matching_exp/relaxed_500_900_6_3/makespan/20151028_003741379816-makespan.csv
python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/complete-relax_500_900_6_3/assignments/20151028_003741250119-assignments.csv -m ./results/matching_exp/complete-relax_500_900_6_3/makespan/20151028_003741250119-makespan.csv
python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/makespan_500_900_6_3/assignments/20151028_003740925671-assignments.csv -m ./results/matching_exp/makespan_500_900_6_3/makespan/20151028_003740925671-makespan.csv

