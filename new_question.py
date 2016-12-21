#! /usr/bin/env python
import os
import argparse
import re

__template = """# {num} - {title}

## Hypothesis

## Test

## Requirements

## Prediction

## Outcome"""


def get_last_question_code(fn):
    questions = [f for f in open(fn) if '[0x' in f]
    last = questions[-1]
    last_code = re.split('\[0x', last)[1].split(' ')[0]
    return last_code


def get_next_code(last_code):
    last_as_int = int(last_code, 16)
    return hex(last_as_int + 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a new research question.")
    parser.add_argument("question")
    args = parser.parse_args()

    direc = '/Users/davison/engd/paperwork/notes/research-questions'
    readme = os.path.join(direc, 'README.md')

    last_code = get_last_question_code(readme)
    next_question_prefix = get_next_code(last_code)

    question = args.question
    question_nospace = question.replace(' ', '-').lower()
    question_link_fmt = '-   [{num} {question}](./{question_nospace}/README.md)\n'
    question_link = question_link_fmt.format(num=next_question_prefix,
                                             question_nospace=question_nospace,
                                             question=question)

    dir_question = os.path.join(direc, question_nospace)
    fn_question = os.path.join(dir_question, "README.md")
    os.mkdir(dir_question)
    with open(fn_question, 'w') as new_file:
        new_file.write(__template.format(num=next_question_prefix,
                       title=question))

    with open(readme, 'a') as f:
        f.write(question_link)
