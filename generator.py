import os
import random
import string

import numpy as np

from config import *

exam_tex_path = src + exam_tex_name
solution_tex_path = src + solution_tex_name
passwords = [''.join(random.choices(string.ascii_letters, k=16)) for _ in range(len(std_ids))]


def get_intersection_bin_count(mapping):
    bins = np.zeros((len(pools) + 1), dtype=int)
    for i, id1 in enumerate(std_ids):
        for j, id2 in enumerate(std_ids):
            if i <= j:
                continue
            bins[np.sum(np.array(mapping[id1]) == np.array(mapping[id2]))] += 1
    return bins


# Create folders
if overwrite_results_folder:
    os.system('rm -r %s || true' % dst)
else:
    os.system('mv %s old_%s 2>/dev/null' % (dst, ''.join(random.choices(string.ascii_letters, k=6))))
os.system('mkdir -p %s && mkdir -p %s' % (exams_dir, solutions_dir))

# Parse the main file
with open(main_tex_path, 'r') as f:
    header, document = f.read().split(hide_solutions_tag)
    beginning, end = document.split(contents_indicator)

# Parse questions
pools = list()
counts = list()
for filename in sorted(os.listdir(pool_dir)):
    if not filename.endswith('.tex'):
        continue
    with open(pool_dir + filename, 'r') as f:
        qs = f.read().split('\\begin{question}')[1:]
        counts.append(len(qs))
        pools.append(['\\begin{question}' + x for x in qs])

# Select questions
qs_stat = np.zeros((len(pools), max(counts)), dtype=int)
student_qs_index_mapping = dict()
student_selected_content = dict()
for std_id in std_ids:
    student_qs_index_mapping[std_id] = list()
    qs = list()
    for pool_idx, pool in enumerate(pools):
        possibles = np.where(qs_stat[pool_idx, :counts[pool_idx]] < len(std_ids) // counts[pool_idx])[0]
        if len(possibles) == 0:
            possibles = np.where(qs_stat[pool_idx, :counts[pool_idx]] == len(std_ids) // counts[pool_idx])[0]
        selected = random.choice(possibles)
        qs.append(pool[selected])
        qs_stat[pool_idx, selected] += 1
        student_qs_index_mapping[std_id].append(selected)
    if shuffle_pools:
        random.shuffle(qs)
    student_selected_content[std_id] = print_after_every_question.join(qs) + print_after_every_question

# Store stats
with open(stats_path, 'w') as f:
    f.write('STD IDs and passwords:\n')
    for pair in zip(std_ids, passwords):
        f.write('%s:\t%s\n' % pair)
    f.write('\n---\n\n')

    f.write('Intersections (Out of %d possible pairs):\n' % (len(std_ids) * (len(std_ids) - 1) / 2))
    intersection_bin_count = get_intersection_bin_count(student_qs_index_mapping)
    for i in range(len(pools) + 1):
        f.write('%d questions:\t%d\n' % (i, intersection_bin_count[i]))
    f.write('\n---\n\n')

    f.write('In how many exams, every question is used?\n')
    for i, count in enumerate(counts):
        f.write('Pool%d:\t' % (i + 1))
        f.write(', '.join(map(str, qs_stat[i, :count])) + '\n')
    f.write('\n---\n\n')

    f.write('Which questions every one of the students is given? (0-based)\n')
    for std_id, qs_index in sorted(student_qs_index_mapping.items()):
        f.write('%s:\t%s\n' % (std_id, ', '.join(map(str, qs_index))))

# Generate tmp tex files and generate pdf outputs
for std_id in std_ids:
    content = student_selected_content[std_id]
    with open(exam_tex_path, 'w') as f:
        f.write('\n'.join([header, hide_solutions_tag, beginning, content, end]))
    if generate_solutions:
        with open(solution_tex_path, 'w') as f:
            f.write('\n'.join([header, beginning, content, end]))

    cwd = os.getcwd()
    os.chdir(src)
    os.system('xelatex -interaction=nonstopmode -output-directory="%s" -jobname=%s "%s"' % (cwd + '/' + exams_dir, std_id, exam_tex_name))
    if generate_solutions:
        os.system('xelatex -interaction=nonstopmode -output-directory="%s" -jobname=%s "%s"' % (cwd + '/' + solutions_dir, std_id, solution_tex_name))
    os.chdir(cwd)

# Compress with passwords
for std_id, password in zip(std_ids, passwords):
    os.system('zip --password %s -j %s%s.zip %s%s.pdf' % (password, exams_dir, std_id, exams_dir, std_id))

# Cleaning up
os.system('rm %s*.log %s*.aux' % (exams_dir, exams_dir))
os.system('rm %s*.log %s*.aux' % (solutions_dir, solutions_dir))
