from EasyDictionary import *

def main():
    while True:
        exit_flag = False

        while True:
            words_input = input("Enter a word or several words separated with commas: ")

            if words_input == '':
                exit_flag = True
                break

            word_list = list(map(lambda w: w.strip(), words_input.split(",")))

            for word in word_list:
                print(oxford_to_quizlet(word))
        
        if exit_flag == True: break


if __name__ == '__main__':
    main()