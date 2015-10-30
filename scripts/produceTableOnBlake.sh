!/bin/bash

# Uniform scores
python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/affinity_500_900_6_3/assignments/20151025_211505622932-assignments.csv -m ./results/matching_exp/affinity_500_900_6_3/makespan/20151025_211505622932-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151025211451/matching_exp_affinity-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151025211451/matching_exp_affinity-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/relaxed_500_900_6_3/assignments/20151025_211505639276-assignments.csv -m ./results/matching_exp/relaxed_500_900_6_3/makespan/20151025_211505639276-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151025211451/matching_exp_relaxed-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151025211451/matching_exp_relaxed-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/complete-relax_500_900_6_3/assignments/20151025_211505634055-assignments.csv -m ./results/matching_exp/complete-relax_500_900_6_3/makespan/20151025_211505634055-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151025211451/matching_exp_complete-relax-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151025211451/matching_exp_complete-relax-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp10-500-900-0.0-0.0-uniform.out ./results/matching_exp/makespan_500_900_6_3/assignments/20151025_211505627063-assignments.csv -m ./results/matching_exp/makespan_500_900_6_3/makespan/20151025_211505627063-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151025211451/matching_exp_makespan-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151025211451/matching_exp_makespan-exp10-500-900-0.5-2.0-uniform.out.log | rev | cut -d ' ' -f1 | rev

# Original Skill Based
python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/affinity_500_900_6_3/assignments/20151022_170140894619-assignments.csv -m ./results/matching_exp/affinity_500_900_6_3/makespan/20151022_170140894619-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151022170125/matching_exp_affinity-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151022170125/matching_exp_affinity-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/relaxed_500_900_6_3/assignments/20151022_170141072512-assignments.csv -m ./results/matching_exp/relaxed_500_900_6_3/makespan/20151022_170141072512-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151022170125/matching_exp_relaxed-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151022170125/matching_exp_relaxed-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/complete-relax_500_900_6_3/assignments/20151022_170140850093-assignments.csv -m ./results/matching_exp/complete-relax_500_900_6_3/makespan/20151022_170140850093-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151022170125/matching_exp_complete-relax-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151022170125/matching_exp_complete-relax-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp1-500-900-0.5-2.0-skill_based.out ./results/matching_exp/makespan_500_900_6_3/assignments/20151022_170140945548-assignments.csv -m ./results/matching_exp/makespan_500_900_6_3/makespan/20151022_170140945548-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151022170125/matching_exp_makespan-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151022170125/matching_exp_makespan-exp1-500-900-0.5-2.0-skill_based.out.log | rev | cut -d ' ' -f1 | rev

# Integer scores
python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/affinity_500_900_6_3/assignments/20151028_003741291372-assignments.csv -m ./results/matching_exp/affinity_500_900_6_3/makespan/20151028_003741291372-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151028003733/matching_exp_affinity-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151028003733/matching_exp_affinity-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/relaxed_500_900_6_3/assignments/20151028_003741379816-assignments.csv -m ./results/matching_exp/relaxed_500_900_6_3/makespan/20151028_003741379816-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151028003733/matching_exp_relaxed-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151028003733/matching_exp_relaxed-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/complete-relax_500_900_6_3/assignments/20151028_003741250119-assignments.csv -m ./results/matching_exp/complete-relax_500_900_6_3/makespan/20151028_003741250119-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151028003733/matching_exp_complete-relax-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151028003733/matching_exp_complete-relax-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp11-500-900-0.5-2.0-integer.out ./results/matching_exp/makespan_500_900_6_3/assignments/20151028_003740925671-assignments.csv -m ./results/matching_exp/makespan_500_900_6_3/makespan/20151028_003740925671-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151028003733/matching_exp_makespan-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151028003733/matching_exp_makespan-exp11-500-900-0.5-2.0-integer.out.log | rev | cut -d ' ' -f1 | rev

# skill and difficulty
python analyzeMatching.py ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out ./results/matching_exp/affinity_500_900_6_3/assignments/20151029_163534669323-assignments.csv -m ./results/matching_exp/affinity_500_900_6_3/makespan/20151029_163534669323-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151029163529/matching_exp_affinity-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151029163529/matching_exp_affinity-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out ./results/matching_exp/relaxed_500_900_6_3/assignments/20151029_163536489057-assignments.csv -m ./results/matching_exp/relaxed_500_900_6_3/makespan/20151029_163536489057-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151029163529/matching_exp_relaxed-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151029163529/matching_exp_relaxed-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out ./results/matching_exp/complete-relax_500_900_6_3/assignments/20151029_163536447774-assignments.csv -m ./results/matching_exp/complete-relax_500_900_6_3/makespan/20151029_163536447774-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151029163529/matching_exp_complete-relax-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151029163529/matching_exp_complete-relax-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev

python analyzeMatching.py ./weights/exp21-500-900-0.5-2.0-skill_and_difficulty.out ./results/matching_exp/makespan_500_900_6_3/assignments/20151029_163536286982-assignments.csv -m ./results/matching_exp/makespan_500_900_6_3/makespan/20151029_163536286982-makespan.csv
grep -F "INFO:root:[SOLVER TIME]" logs/20151029163529/matching_exp_makespan-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev
grep -F "INFO:root:[TOTAL TIME]" logs/20151029163529/matching_exp_makespan-exp21-500-900-0.5-2.0-skill_and_difficulty.out.log | rev | cut -d ' ' -f1 | rev
