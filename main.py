# Lab Exeample
# data = [["A", "B", "(FG)", "C", "D"],
#           ["B", "G", "D"],
#           ["B", "F", "G", "(AB)"],
#           ["F", "(AB)", "C", "D"],
#           ["A", "(BC)", "G", "F", "(DE)"]]


# Lecture Example
data = [["(bd)","c","b"],
        ["(bf)", "(ce)","b"],
        ["(ag)","b"],
        ["(be)","(ce)"],
        ["a","(bd)","b","c","b"]]


# Generate  candidates  1-item sequence


def gen_cand1(data):
    cand1 = []

    for i in range(0, len(data)):
        seq = data[i]

        for j in range(0, len(seq)):
            element = seq[j]

            for k in range(0, len(element)):
                if ((element[k] in cand1) == False):
                    cand1.append(element[k])

    cand1.remove('(')
    cand1.remove(')')
    return cand1




#__________________________________________________________________________________________________________________________________________________________________________________

 # Generate candidates 2-item sequences
def gen_cand2(frequent1):

  cand2 = []

  l1 = frequent1
  l2 = l1

# All possible Temporal  joins
  for i in range(0,len(l1)):
    l1_item = l1[i]
    for j in range(0, len(l2)):
      l2_item = l2[j]
      cand2.append(l1_item + l2_item)

# All possible non-Temporal  joins
  for i in range(1, len(l1)): # i = 1 ; i < len(l); i++
    l1_item = l1[i]
    for j in range(0, i):
       l2_item = l2[j]
       cand2.append("(" + l2_item + l1_item + ")")

  return cand2


#__________________________________________________________________________________________________________________________________________________________________________________



def swap(str, i, j):
   list1 = list(str)
   list1[i], list1[j] = list1[j], list1[i]
   return ''.join(list1)


# Generate candidates of k-item squences (k > 2):

def gen_candK(frequentk, k):
    h = 2 - k
    candk = []
    l = []

    # AB BC  => ABC K = 3
    # ABC BCD => ABCD

    i = 0  # index of items insed frequentk
    j = 0  # index of inner list inside l

    while (i < len(frequentk)):

        orig_item = right_item = left_item = frequentk[i]

        t = 0

        # CASE 1
        if ((orig_item[0] == '(') and (orig_item[-1] == ')')):
            for k in range(1, (len(orig_item) - 1)):

                l.insert(j, [])
                l[j].append(orig_item)

                left_item = swap(left_item, 1, k)
                right_item = swap(right_item, -2, -2 - t)  # (ABF) AFB  BFA

                if (len(orig_item) == 4):  # lke (AB) here we will not put expanded characters inside ()

                    l[j].append(left_item[2:-1])  # remain after removeing first character
                    l[j].append(right_item[1:-2])  # remain after removing last character

                else:

                    l[j].append('(' + left_item[2:-1] + ')')  # remain after removeing first character
                    l[j].append('(' + right_item[1:-2] + ')')  # remain after removeing last characte

                t = t + 1
                j = j + 1

        # CASE 2
        elif (orig_item[0] == '('):  # (AFERF)XG (AfdkfF)X
            rbi = orig_item.index(')')  # right brace index
            for m in range(1, rbi):

                left_item = swap(left_item, 1, m)

                l.insert(j, [])
                l[j].append(orig_item)

                if ((rbi + 1) == 4):
                    l[j].append(left_item[2: rbi] + left_item[(rbi + 1):])  # remain after removeing first character

                else:
                    l[j].append(
                        '(' + left_item[2: rbi] + ')' + left_item[(rbi + 1):])  # remain after removeing first character

                l[j].append(right_item[:-1])  # remain after removing last character

                j = j + 1

        # CASE 3
        elif (orig_item[-1] == ')'):  # XG(ABF)

            rbi = len(orig_item) - 1  # right brace index
            lbi = orig_item.index('(')  # right brace index

            for c in range((lbi + 1), rbi):

                right_item = swap(right_item, -2, -2 - t)

                l.insert(j, [])
                l[j].append(orig_item)
                l[j].append(left_item[1:])  # remain after removeing last character

                if ((rbi - lbi + 1) == 4):
                    l[j].append(right_item[:lbi] + right_item[lbi + 1:-2])

                else:
                    l[j].append(right_item[:lbi] + '(' + right_item[lbi + 1: rbi - 1] + ')')

                t = t + 1
                j = j + 1

        # CASE 4
        else:  # XG(ABF)LM OR XGFM
            l.insert(j, [])
            l[j].append(orig_item)
            l[j].append(orig_item[1:])
            l[j].append(orig_item[:-1])
            j = j + 1

        i = i + 1




    for i in range(0, len(l)):

        for j in range(0, len(l)):
            if (l[i][0] == l[j][0]):
                continue;

            if (l[i][1] == l[j][2]):
                if (l[j][0][0] == '('):
                    out = l[i][0][:h] + l[j][0]
                else:
                    out = l[i][0] + l[j][0][(-1 * h):]
                if (out not in candk): candk.append(out)

    return candk

#__________________________________________________________________________________________________________________________________________________________________________________

# calculate support of candidates
def calc_support(data, cand):
    supp_count = 0
    cand_sup = {}
    brace_item = "$"
    end_index = 0
    char_found_count = 0

    for cand_item in cand:
        cand_item_len = len(cand_item)

        for seq_count in range(0, len(data)):
            seq = data[seq_count]

            if (char_found_count == cand_item_len):
                supp_count = supp_count + 1

            char_found_count = 0  # number of founded character of cand_item
            cand_char_index = 0  # index of cand character i search for

            seq_item_count = 0
            while (seq_item_count < len(seq)):
                seq_item = seq[seq_item_count]

                if ((brace_item in seq_item) == True):
                    brace_item = "$"
                    char_found_count = end_index
                    cand_char_index = end_index
                    seq_item_count = seq_item_count + 1
                    continue

                if (cand_char_index >= cand_item_len):
                    break

                seq_item_char_count = 0
                while (seq_item_char_count < len(seq_item)):

                    seq_item_char = seq_item[seq_item_char_count]  # current character in current sequence item
                    cand_char = cand_item[cand_char_index]  # current char i search for in candidate item

                    if (cand_char != '('):
                        if (seq_item_char == '('):

                            if ((cand_char in seq_item) == True):
                                char_found_count = char_found_count + 1
                                cand_char_index = cand_char_index + 1
                                break


                        else:
                            if (cand_char == seq_item_char):
                                char_found_count = char_found_count + 1
                                cand_char_index = cand_char_index + 1

                        # if (cand_char_index >= cand_item_len):
                        #     break

                    else:
                        if (brace_item == '$'):
                            seq_item_count = seq_item_count - 1
                        end_index = cand_item[char_found_count:].index(')') + char_found_count + 1
                        brace_item = cand_item[char_found_count:end_index]
                        break

                    seq_item_char_count = seq_item_char_count + 1

                seq_item_count = seq_item_count + 1

        if (char_found_count == cand_item_len):
            supp_count = supp_count + 1

        cand_sup[cand_item] = supp_count
        supp_count = 0
        char_found_count = 0  # number of founded character of cand_item
        cand_char_index = 0  # index of cand character i search for

    return cand_sup



#__________________________________________________________________________________________________________________________________________________________________________________



# support pruning

def support_pruning(cand_sup, min_sup, cand):

  for key in list(cand_sup):
    if(cand_sup[key] < min_sup):
      cand.remove(key)


  return cand

#__________________________________________________________________________________________________________________________________________________________________________________

def main():
    # local variables
    min_sup = 2
    k = 3

    # 1-item sequences
    cand1 = gen_cand1(data)
    cand1_support = calc_support(data, cand1)
    frequent1 = support_pruning(calc_support(data, gen_cand1(data)), 2, cand1)

    print("Frequent 1-item Sequences =>>  ", frequent1)

    # 2-items sequences
    cand2 = gen_cand2(frequent1)
    cand2_support = calc_support(data, cand2)
    frequent2 = support_pruning(calc_support(data, cand2), 2, cand2)

    print("Frequent 2-item Sequences =>>  ", frequent2)

    # k-items sequences (k > 2)
    frequent = frequent2
    while (True):

        cand = gen_candK(frequent, k)

        if (len(cand) == 0):
            break

        cand_support = calc_support(data, cand)
        frequent = support_pruning(cand_support, min_sup, cand)

        print("Frequent {}-item Sequences =>>  ".format(k), frequent)

        k = k + 1


#__________________________________________________________________________________________________________________________________________________________________________________




main()





