from autograder import Autograder
import json, os, shutil

DEBUG = False

def main():
    CWD = os.getcwd()
    TMP_FOLDER = os.path.join(CWD, 'tmp')
    STUDENT_SRC_FOLDER = os.path.join(TMP_FOLDER, 'src')
    BUILD_FOLDER = os.path.join(TMP_FOLDER, 'build')

    # copy student code from /autograder/submission to a temp folder
    if os.path.exists(TMP_FOLDER):
        shutil.rmtree(TMP_FOLDER)
    shutil.copytree('/autograder/submission/', STUDENT_SRC_FOLDER)
    os.mkdir(BUILD_FOLDER)

    # create new autograder object from config
    autograder = Autograder("../autograder_config.yml", STUDENT_SRC_FOLDER, BUILD_FOLDER)

    # try to compile student code -- results are in autograder.compiler.results
    autograder.compiler.run_test()
    if DEBUG:
        print(autograder.compiler.results)
    with open(os.path.join(TMP_FOLDER, 'compile_commands.json'), 'w+') as outfile:
        json.dump(autograder.compiler.compile_commands, outfile)

    # run linter
    if autograder.linter:
        autograder.linter.run_test()
        if DEBUG:
            print(autograder.linter.results)

    # run formatter

    # run test cases (get json output from googletest)
    autograder.tester.run_test()
    if DEBUG:
        print(autograder.tester.results)

    # create json object with overall results and write to results directory
    with open('/autograder/results/results.json', 'w+') as outfile:
        outfile.write(autograder.make_json())


if __name__ == '__main__':
    main()
