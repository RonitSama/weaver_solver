import re
import time
from pprint import pformat
from functools import lru_cache
from node import Node
from solve_on_site import SiteSolver
from word_bank import bank

NUM_LETTERS = 4
interval: int
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
                bank.pop(solver.get_incorrect_word().lower(), None)
                with open('word_bank.py', 'w') as bank_update:
                    bank_update.write('bank = {{\n {}'.format(pformat(bank)[1:]))
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


# @lru_cache
def get_matches(word: str, skip: int = None) -> list[str]:
    matches = bank[word.lower()].copy()
    if skip is not None and 0 <= skip <= 3:
        pattern = f'{word[:skip]}.{word[skip+1:]}'
        matches = {poss_match for poss_match in matches if ((not re.match(pattern.upper(), poss_match)) and poss_match.lower() in bank)}
    
    # prioritize matches that get green
    matches = sorted(list(matches), key=find_green, reverse=True)

    return matches


def solve(current_word: str, current_path_length: int = 0, index_just_changed: int = 5, test: bool = False):
    global optimal, solved, not_good_path, trying, poss_found, root

    # only executed once a solution is found, but hasn't been
    # truly tested
    if test:
        solved = True
        root.set_path(trying)

        # solution goes in solution.txt
        with open('solution.txt', 'w') as solution:
            solution.write(f'{root}\n')

    if solved:
        return

    # if end_word is reached, end
    if current_word == end_word:
        with open('solution.txt', 'w') as solution:
            solution.write(str(root) + '\n')
        solved = True

    if solved:
        return

    # if the current path won't reach the end word in the optimal, stop
    if current_path_length >= optimal - 2 and find_green(current_word) <= 1:
        return True

    # solution is found
    if len(root) == optimal - 1 and \
        find_green(root.get_value_at(-1)) == 3 and \
            not solved:
        # if condition explained:
        # current path length is 1 away from the optimal and the number
        # of green letters in the current word is 1 away from being the
        # final word, the solution is found
        solved = True
        root.add_node(end_word)
        with open('solution.txt', 'w') as solution:
            solution.write(str(root) + '\n')
        return

    # if current path length is the optimal, end and go back
    # if it was the correct path, it would have been solved 1 recursive
    # call before
    if current_path_length >= optimal:

        # if the path is 1 away, save it for next optimal
        if find_green(current_word) == 3:
            if not poss_found:
                trying = root.as_list(include=True).append(end_word)
                poss_found = True

        return

    # current path is still okay, but not solved
    # so find next words to continue checking
    matches = get_matches(current_word, index_just_changed)

    # iterate each match
    for match in matches:

        # handling recursion mismatch
        if find_difference(root.get_value_at(-1), match) != 1:
            # if the matches don't match the last word in the Linked
            # List, flow of control is incorrect
            return

        # add a new node containing the current word
        root.add_node(match)

        # easiest way to communicate between recursive calls
        not_good_path = solve(match, len(root),
                              find_changed_index(match, current_word))
        if not_good_path is not None:
            break

        # many (if solved: return)'s all across function
        if solved: 
            return

        # still in loop, so cut off current match being checked to
        # allow for checking next match
        root.cut_nodes_at(value_to_remove=match)

    if solved:
        return

    # cut nodes off, current word is incorrect
    root.cut_nodes_at(value_to_remove=current_word,
                      keep=not_good_path)

    # increments optimal after every path is checked
    if current_word == start_word:
        optimal += 1
        solve(start_word, 0, test=True if trying is not None and len(
            trying) > 0 else False)


if __name__ == '__main__':
    main()
