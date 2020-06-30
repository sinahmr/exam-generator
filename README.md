# Exam Generator

Given the current circumstances and due to the COVID-19 pandemic, the university exams are being held online.
Some courses use the traditional way of taking an exam: They provide students with a PDF containing questions, students should answer the questions and submit
a scanned copy of their answers. Because of this situation, it is necessary to have multiple different exams for different students in the class.

This project generates a random set of problems for every student, given multiple pools of questions. The number of questions in each exam is equal to the number of pools.

Questions will be placed in the main TeX file, in replacement of `% CONTENT %` string. You can change this arbitrary string in the [config](config.py) file.
Also in that file:
- `std_ids` is the list of Student IDs;
- `print_after_every_question` will be placed in the TeX files, after every question;
- `overwrite_results_folder` controls whether to remove or rename the results folder;
- `shuffle_pools` controls whether the order of pools should be preserved or should the questions get shuffled in every exam paper;
- `compress` controls whether zip outputs should be created, using a random password for each student.

Questions of every pool are distributed almost uniformly in all the exam papers, and the maximum number of differences in their occurrence is 1.

If your TeX file has a specific tag for showing or hiding solutions, you may set `hide_solutions_tag` to that tag and also `generate_solutions` to `True` (In the [config](config.py) file).

Before generating the actual PDFs, a stats file will be created containing the following information:
- The mapping of student IDs and zip files' generated passwords (If `compress == True`).
- Out of every pair of the exams, how many of them have `i` questions in common? (With `i` varying from 0 to the number of questions in each exam)
- In how many exams, every question is used?
- Which questions every one of the students is given? (0-based)

You can see an example valid TeX project in the [example_tex](example_tex) folder, and example generated exams in [example_results](example_results) folder.

Note: You shouldn't use tags like `\iffalse` and `\fi` in pool files in order to remove a question. Every `\begin{question}` tag will be considered as a valid question.
