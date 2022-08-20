import EasyDictionary

def main():
    while True:
        exit_flag = False

        while True:
            words_input = input("Enter a word or several words separated with commas: ")

            if words_input == '':
                exit_flag = True
                break

            word_list = list(map(lambda w: w.strip(), words_input.split(",")))

            for i in range(len(word_list)):
                word_set = EasyDictionary.get_word_set_from_oxford(word_list[i], True)
                word_set = EasyDictionary.modify_examples(word_set)
                word_list[i] = word_set
                
                print(word_list[i])
        
        if exit_flag == True: break


if __name__ == '__main__':
    main()