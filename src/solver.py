import re
import time
from pprint import pformat
from functools import lru_cache
from node import Node
from solve_on_site import SiteSolver
from word_bank import bank

NUM_LETTERS = 4
root: Node
start_word: str
end_word: str
optimal: int
solved: bool
trying: list[str]
poss_found: bool
not_good_path: bool


def main():
    global solved, trying, optimal, poss_found, end_word, not_good_path, root, start_word, end_word

    ans = input('Automate? (y/n/t):  ')
    '''Response:
    ------------
    y or a - solves today's challenge, then continues to random new
        challenges indefinitely
    n - allows user to input custom words, must be 4 letters each
    t - solves today's challenge only
    '''
    auto = True if ans.lower() == 'y' or ans.lower() == 'a' else False
    if auto or (ans == 't'):
        solver = SiteSolver()

    while True:
        solved = False
        trying = []
        optimal = 4
        poss_found = False
        not_good_path = None

        # get start word
        if auto or (ans == 't'):
            start_word = solver.start
            end_word = solver.end
        else:
            start_word = input('Starting word:  ').upper()
            end_word = input('Ending word:    ').upper()
            assert len(start_word) == 4 and len(end_word) == 4, \
                "Both words must be 4 characters in length."

        root = None
        root = Node(start_word, 0, True)

        # solve
        solve(start_word, 0)
        if hasattr(solve, 'recursion'):
            del solve.recursion

        # found optimal goes in terminal
        print(len(root))

        if 'solver' in locals():
            solver.solve(root.as_list())
            time.sleep(2)
            try:
                if auto:
                    solver.click_random()
                    continue
                else:
                    break
            except ValueError:
                # fix wrong answer
                bank.remove(solver.get_incorrect_word().lower())
                with open('word_bank.py', 'w') as bank_update:
                    bank_update.write(f'bank = [\n {pformat(bank)[1:]}')
                solver.delete_all(len(root))
        else:
            break


@lru_cache
def is_green(word: str, index: int) -> bool:
    if index > NUM_LETTERS:
        return False
    return word[index] == end_word[index]


@lru_cache
def find_green(word: str) -> int:
    green = [is_green(word, i) for i in range(NUM_LETTERS)]
    total = 0
    for letter in green:
        total += 1 if letter else 0
    return total


@lru_cache
def find_changed_index(word: str, original: str) -> int:
    for i in range(NUM_LETTERS):
        if word[i] != original[i]:
            return i


@lru_cache
def find_difference(word_1: str, word_2: str) -> int:
    diff = NUM_LETTERS
    for i in range(NUM_LETTERS):
        if word_1[i] == word_2[i]:
            diff -= 1
    return diff


@lru_cache
def find_matches(word: str, skip: int = None) -> list[str]:
    matches = []

    # go through each index (4)
    for i in range(NUM_LETTERS):
        if i == skip:
            continue

        # find matches
        pattern = f'{word[:i]}.{word[i+1:]}'
        matches.extend([word.upper() for word in bank if
                        re.match(pattern.lower(), word) and
                        word.upper() != word and
                        word.upper() not in root.as_list() and
                        not word.upper() == root.value])

    # prioritize matches that get green
    num_green = [find_green(match) for match in matches]
    for i in range(len(matches)):
        for j in range(len(matches)):
            if num_green[j] > num_green[i]:
                matches[i], matches[j] = matches[j], matches[i]

    return matches


def solve(current_word: str, current_path_length: int = 0, index_just_changed: int = 5, test: bool = False):
    global optimal, solved, not_good_path, trying, poss_found, root

    if test:
        solved = True
        root.set_path(trying)
        with open('solution.txt', 'w') as solution:
            solution.write(f'{root}\n')

    if solved:
        return

    matches = []

    # if end_word is reached, end
    if current_word == end_word:
        with open('solution.txt', 'w') as solution:
            solution.write(str(root) + '\n')
        solved = True

    if solved:
        return

    if current_path_length >= optimal - 2 and find_green(current_word) == 0:
        return True

    if len(root) == optimal - 1 and find_green(root.get_value_at(-1)) == 3 and not solved:
        solved = True
        root.add_node(end_word)
        with open('solution.txt', 'w') as solution:
            solution.write(str(root) + '\n')
        return

    # if current path length is the optimal, end and go back
    if current_path_length >= optimal:
        # if the path is 1 away, save it for next optimal
        if find_green(current_word) == 3:
            if not poss_found:
                trying = root.as_list(include=True).append(end_word)
                poss_found = True

        return

    matches = find_matches(current_word, index_just_changed)

    # iterate each match
    for match in matches:
        if find_difference(root.get_value_at(-1), match) != 1:
            return

        # add a new node containing the current word
        root.add_node(match)

        not_good_path = solve(match, len(
            root), find_changed_index(match, current_word))
        if not_good_path is not None:
            break
        if solved:
            return

        root.cut_nodes_at(value_to_remove=match)

    if solved:
        return

    # cut nodes off
    root.cut_nodes_at(value_to_remove=current_word,
                      keep=not_good_path)

    if current_word == start_word:
        optimal += 1
        solve(start_word, 0, test=True if trying is not None and len(
            trying) > 0 else False)


if __name__ == '__main__':
    main()
