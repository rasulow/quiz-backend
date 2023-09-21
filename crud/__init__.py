from crud.group import read_groups, create_group, delete_group
from crud.student import read_student, delete_student
from crud.subject import read_subject, create_subject, delete_subject
from crud.exam import (read_exam, create_exam, delete_exam, update_status, 
                       get_active_exams, get_passed_exams, get_current_exam,
                       get_exam_results)
from crud.question import (read_question, create_question, delete_question,
                           get_current_exam_questions, check_result_of_exam)