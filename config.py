# Files and directories
src = 'example_tex/'
pool_dir = src + 'pools/'
main_tex_path = src + 'main.tex'
exam_tex_name = 'tmp_exam.tex'
solution_tex_name = 'tmp_solution.tex'

dst = 'example_results/'
exams_dir = dst + 'exams/'
solutions_dir = dst + 'solutions/'

stats_path = 'example_stats.txt'

# Student IDs
std_ids = ['0001', '0002', '0003']

# Options
print_after_every_question = '\n\n\hrulefill'

content_indicator = '% CONTENT %'

generate_solutions = True
hide_solutions_tag = '\hidesolutions'

overwrite_results_folder = True
shuffle_pools = True
compress = True
