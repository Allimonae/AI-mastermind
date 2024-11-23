"""
Knowledge Base
"""

from scsa import read_from_file
# import random 
# from ABC import ABC, abstractmethod

class Features:
    def __init__(self, code):
        self.colors = [] # colors used in the code
        self.number_of_colors = 0 # how many colors used in the code
        self.pattern = "None"

        # initialize self.colors
        for element in code:
            if element not in self.colors:
                self.colors.append(element)

        # initialize self.number_of_colors
        self.number_of_colors = len(self.colors)

        # initialize self.pattern
        self.pattern = self.check_pattern(code)

    # given a code, find a repeating pattern
    def check_pattern(self, code):
        n = len(code)
        for pattern_length in range(1, n // 2 + 1):  # Pattern length can be at most half of the string
            pattern = code[:pattern_length]
            num_repeats = n // pattern_length
            
            # Check if the pattern repeated multiple times matches the original string
            if pattern * num_repeats == code[:num_repeats * pattern_length]:
                if len(pattern) == 1:
                    repeating_pattern = "Mono"
                else:
                    repeating_pattern = f"{len(pattern)} repeating"

                # return the type of repeating pattern
                return repeating_pattern

        # No pattern found
        return "None"

    def print_features(self):
        print(f"Colors:{self.colors}, Number of Colors: {self.number_of_colors}, Pattern: ")

class KnowledgeBase(Features):
    def __init__(self):
        self.colors_counts = {} # dictionary of colors ordered by counts
        self.number_of_colors_counts = {} # dictionary of number of colors ordered by counts
        self.number_of_data = 0 # how many data values are in the knowledge base
        self.patterns = {} # patterns found

        # for i, c in enumerate(colors):
        #     self.colors_counts[c] = 0
        #     self.number_of_colors_counts[i + 1] = 0

    # given a code, find features and add to knowledge base
    def update_kb(self, code):
        features = Features(code) # find features
        self.number_of_data += 1 # increment data count

        # update colors_count
        for element in features.colors:
            if element not in self.colors_counts:
                self.colors_counts[element] = 0
            self.colors_counts[element] += 1

        # update number_of_colors_count
        if features.number_of_colors not in self.number_of_colors_counts:
            self.number_of_colors_counts[features.number_of_colors] = 0
        self.number_of_colors_counts[features.number_of_colors] += 1
        
        # update patterns
        if features.pattern not in self.patterns:
            self.patterns[features.pattern] = 0
        self.patterns[features.pattern] += 1
        
        # order probabilities by most to least likely
        self.colors_counts = dict(sorted(self.colors_counts.items(), key=lambda item: item[1], reverse=True))
        self.number_of_colors_counts = dict(sorted(self.number_of_colors_counts.items(), key=lambda item: item[1], reverse=True))
        self.patterns = dict(sorted(self.patterns.items(), key=lambda item: item[1], reverse=True))

    # given a file name, make a Knowledge base
    def make_kb(self, file_name):
        for code in read_from_file(file_name):
            self.update_kb(code)

    def print_kb(self):
        print(f"Colors Counts:{self.colors_counts}\nNum Colors Counts:{self.number_of_colors_counts}\nPatterns:{self.patterns}\n")

def main():
    kb1 = KnowledgeBase()
    # print(kb1.colors_counts)
    kb1.make_kb("Mystery1_10_7_200.txt")
    print("Mystery SCSA: Mystery1_10_7_200.txt")
    kb1.print_kb()

    # kb2 = KnowledgeBase()
    # kb2.make_kb("Mystery2_10_7_200.txt")
    # print("Mystery SCSA: Mystery2_10_7_200.txt")
    # kb2.print_kb()

    # kb3 = KnowledgeBase()
    # kb3.make_kb("Mystery3_10_7_200.txt")
    # print("Mystery SCSA: Mystery3_10_7_200.txt")
    # kb3.print_kb()

    # kb4 = KnowledgeBase()
    # kb4.make_kb("Mystery4_10_7_200.txt")
    # print("Mystery SCSA: Mystery4_10_7_200.txt")
    # kb4.print_kb()

    # kb5 = KnowledgeBase()
    # kb5.make_kb("Mystery5_10_7_200.txt")
    # print("Mystery SCSA: Mystery5_10_7_200.txt")
    # kb5.print_kb()

if __name__ == "__main__":
    main()
