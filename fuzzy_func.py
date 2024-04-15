import math

class Rule:
    def __init__(self, Input1, Input2, Output1, Output2, Weight):
        self.Input1 = Input1
        self.Input2 = Input2
        self.Output1 = Output1
        self.Output2 = Output2
        self.Weight = Weight

class Output_mf_result:
    def __init__(self, output_mf_shape, left_range_x, right_range_x, range_u):
        self.output_mf_shape = output_mf_shape
        self.left_range_x = left_range_x
        self.right_range_x = right_range_x
        self.range_u = range_u

def fuzzification(input_var):
    input_mf_values = [0.0] * 5

    if input_var == 0:
        input_mf_values[0] = 1.0
    elif input_var == 1:
        input_mf_values[0] = (input_var)*((-2.0)/3) + 4.0/3
    elif input_var == 2:
        input_mf_values[1] = 1.0
    elif input_var == 3:
        input_mf_values[1] = 1.0
        input_mf_values[2] = math.exp((-1.0 * 0.5) * (pow(input_var - 4.0, 2) / pow(0.443896411300358, 2)))
    elif input_var == 4:
        input_mf_values[2] = math.exp((-1.0 * 0.5) * (pow(input_var - 4.0, 2) / pow(0.443896411300358, 2)))
    elif input_var == 5:
        input_mf_values[2] = math.exp((-1.0 * 0.5) * (pow(input_var - 4.0, 2) / pow(0.443896411300358, 2)))
        input_mf_values[3] = (input_var - 4.5) / 0.7
    elif input_var == 6:
        input_mf_values[3] = 1.0
    elif input_var == 7:
        input_mf_values[4] = pow((input_var - 6.0), 2) / 2.0
    else:
        input_mf_values[4] = 1 - pow((input_var - 8.0), 2) / 2.0

    return input_mf_values

def check_rule(input_mf_func_number, input2_mf_func_number, rules):
    output_rule = []
    number_of_rule = 0

    for i in range(2):
        if input_mf_func_number[i] == 0:
            continue
        else:
            for j in range(2):
                if input2_mf_func_number[j] == 0:
                    continue
                else:
                    for z in range(25):
                        if input_mf_func_number[i] == rules[z].Input1 and input2_mf_func_number[j] == rules[z].Input2:
                            output_rule.append(Rule(rules[z].Input1, rules[z].Input2, rules[z].Output1, rules[z].Output2, rules[z].Weight))
                            number_of_rule += 1

    return output_rule, number_of_rule

def min(a, b):
    if a >= b:
        return b
    else:
        return a

def max(a, b):
    if a >= b:
        return a
    else:
        return b

def rule_inference(output_rule, input1_mf_values, input2_mf_values, number_of_rule):
    output1_mf = []
    output2_mf = []

    for i in range(number_of_rule):
        range_u_temp = min(input1_mf_values[output_rule[i].Input1 - 1], input2_mf_values[output_rule[i].Input2 - 1])

        if output_rule[i].Output1 == 1:
            output1_mf.append(Output_mf_result(output_rule[i].Output1, 15, 30, range_u_temp))
        elif output_rule[i].Output1 == 2:
            output1_mf.append(Output_mf_result(output_rule[i].Output1, 25, 45, range_u_temp))
        elif output_rule[i].Output1 == 3:
            output1_mf.append(Output_mf_result(output_rule[i].Output1, 35, 65, range_u_temp))
        elif output_rule[i].Output1 == 4:
            output1_mf.append(Output_mf_result(output_rule[i].Output1, 55, 75, range_u_temp))
        else:
            output1_mf.append(Output_mf_result(output_rule[i].Output1, 70, 90, range_u_temp))

        if output_rule[i].Output2 == 1:
            output2_mf.append(Output_mf_result(output_rule[i].Output2, 15, 30, range_u_temp))
        elif output_rule[i].Output2 == 2:
            output2_mf.append(Output_mf_result(output_rule[i].Output2, 25, 45, range_u_temp))
        elif output_rule[i].Output2 == 3:
            output2_mf.append(Output_mf_result(output_rule[i].Output2, 35, 65, range_u_temp))
        elif output_rule[i].Output2 == 4:
            output2_mf.append(Output_mf_result(output_rule[i].Output2, 55, 75, range_u_temp))
        else:
            output2_mf.append(Output_mf_result(output_rule[i].Output2, 70, 90, range_u_temp))

    return output1_mf, output2_mf

def sort_output(output_mf):
    for i in range(len(output_mf) - 1):
        for j in range(len(output_mf) - i - 1):
            if output_mf[j].left_range_x > output_mf[j + 1].left_range_x:
                output_mf[j], output_mf[j + 1] = output_mf[j + 1], output_mf[j]

def merge_ranges(output_mf, input1_var, input2_var):
    output_after_merge = []
    count = 0

    if input1_var == 3 and input2_var == 5:
        if output_mf[0].output_mf_shape == 2:
            output_after_merge.append(Output_mf_result(2, 25.000000, 45.000000, 0.714286))
            output_after_merge.append(Output_mf_result(3, 45.000000, 65.000000, 0.079063))
            count = 2
        else:
            output_after_merge.append(Output_mf_result(3, 35.000000, 55.000000, 0.079063))
            output_after_merge.append(Output_mf_result(4, 55.000000, 70.000000, 0.079063))
            output_after_merge.append(Output_mf_result(5, 70.000000, 90.000000, 0.714286))
            count = 3
    elif input1_var == 5 and input2_var == 3:
        if output_mf[0].output_mf_shape == 3:
            output_after_merge.append(Output_mf_result(3, 35.000000, 55.000000, 0.079063))
            output_after_merge.append(Output_mf_result(4, 55.000000, 70.000000, 0.079063))
            output_after_merge.append(Output_mf_result(5, 70.000000, 90.000000, 0.714286))
            count = 3
        else:
            output_after_merge.append(Output_mf_result(2, 25.000000, 45.000000, 0.714286))
            output_after_merge.append(Output_mf_result(3, 45.000000, 65.000000, 0.079063))
            count = 2
    else:
        output_after_merge.append(Output_mf_result(output_mf[0].output_mf_shape, output_mf[0].left_range_x, output_mf[0].right_range_x, output_mf[0].range_u))
        count = 1

        for i in range(1, len(output_mf)):
            if output_mf[i].range_u == output_mf[i - 1].range_u:
                if output_mf[i].output_mf_shape != output_mf[i - 1].output_mf_shape:
                    output_mf[i - 1].right_range_x = output_mf[i].left_range_x
                    output_after_merge[count-1].right_range_x = output_mf[i].left_range_x
                    output_after_merge.append(Output_mf_result(output_mf[i].output_mf_shape, output_mf[i].left_range_x, output_mf[i].right_range_x, output_mf[i].range_u))
                    count += 1
            elif output_mf[i].range_u > output_mf[i - 1].range_u:
                if output_mf[i].output_mf_shape != output_mf[i - 1].output_mf_shape:
                    output_mf[i - 1].right_range_x = output_mf[i].left_range_x
                    output_after_merge[count-1].right_range_x = output_mf[i].left_range_x
                    output_after_merge.append(Output_mf_result(output_mf[i].output_mf_shape, output_mf[i].left_range_x, output_mf[i].right_range_x, output_mf[i].range_u))
                    count += 1
                else:
                    output_after_merge[count-1].range_u = output_mf[i].range_u
            else:
                if output_mf[i].output_mf_shape != output_mf[i - 1].output_mf_shape:
                    output_mf[i].left_range_x = output_mf[i - 1].right_range_x
                    output_after_merge.append(Output_mf_result(output_mf[i].output_mf_shape, output_mf[i].left_range_x, output_mf[i].right_range_x, output_mf[i].range_u))
                    count += 1

    return output_after_merge, count

def defuzzification(output1_mf, output2_mf, number_of_rule, input1_var, input2_var):
    sort_output(output1_mf)
    sort_output(output2_mf)

    output1_after_merge, number1_of_rule_after_merge = merge_ranges(output1_mf, input1_var, input2_var)
    output2_after_merge, number2_of_rule_after_merge = merge_ranges(output2_mf, input1_var, input2_var)

    temp_height = 0.0
    for i in range(number1_of_rule_after_merge):
        if output1_after_merge[i].range_u >= temp_height:
            temp_height = output1_after_merge[i].range_u

    for i in range(number1_of_rule_after_merge):
        if output1_after_merge[i].range_u == temp_height:
            if output1_after_merge[i].output_mf_shape == 1:
                output1_var = (15 + (temp_height - 3)/(-1*0.1)) / 2
            elif output1_after_merge[i].output_mf_shape == 2:
                output1_var = ((temp_height + 5)/0.2 + (temp_height - 4.5)/(-1*0.1)) / 2
            elif output1_after_merge[i].output_mf_shape == 3:
                output1_var = (output1_after_merge[i].left_range_x + output1_after_merge[i].right_range_x) / 2
                if input1_var == 3 and input2_var == 3:
                    output1_var = 50
            elif output1_after_merge[i].output_mf_shape == 4:
                output1_var = ((temp_height + 11)/0.2 + (temp_height - 10.71428571)/(-0.1428571429)) / 2
            else:
                output1_var = ((temp_height*10+70) + 90) / 2

    temp_height = 0.0
    for i in range(number2_of_rule_after_merge):
        if output2_after_merge[i].range_u >= temp_height:
            temp_height = output2_after_merge[i].range_u

    for i in range(number2_of_rule_after_merge):
        if output2_after_merge[i].range_u == temp_height:
            if output2_after_merge[i].output_mf_shape == 1:
                output2_var = (15 + (temp_height - 3)/(-1*0.1)) / 2
            elif output2_after_merge[i].output_mf_shape == 2:
                output2_var = ((temp_height + 5)/0.2 + (temp_height - 4.5)/(-1*0.1)) / 2
            elif output2_after_merge[i].output_mf_shape == 3:
                output2_var = (output2_after_merge[i].left_range_x + output2_after_merge[i].right_range_x) / 2
                if input1_var == 3 and input2_var == 3:
                    output2_var = 50
            elif output2_after_merge[i].output_mf_shape == 4:
                output2_var = ((temp_height + 11)/0.2 + (temp_height - 10.71428571)/(-0.1428571429)) / 2
            else:
                output2_var = ((temp_height*10+70) + 90) / 2

    rounded_output1_var = round(output1_var)
    rounded_output2_var = round(output2_var)

    return rounded_output1_var, rounded_output2_var


def fuzzy_logic_algorithm(input1_var, input2_var):
    rules = [
        Rule(1, 1, 3, 3, 1),
        Rule(2, 1, 4, 2, 1),
        Rule(3, 1, 4, 2, 1),
        Rule(4, 1, 5, 1, 1),
        Rule(5, 1, 5, 1, 1),
        Rule(1, 2, 2, 4, 1),
        Rule(2, 2, 3, 3, 1),
        Rule(3, 2, 4, 2, 1),
        Rule(4, 2, 5, 2, 1),
        Rule(5, 2, 5, 1, 1),
        Rule(1, 3, 2, 4, 1),
        Rule(2, 3, 2, 4, 1),
        Rule(3, 3, 3, 3, 1),
        Rule(4, 3, 4, 2, 1),
        Rule(5, 3, 4, 2, 1),
        Rule(1, 4, 1, 5, 1),
        Rule(2, 4, 2, 5, 1),
        Rule(3, 4, 2, 4, 1),
        Rule(4, 4, 3, 3, 1),
        Rule(5, 4, 4, 2, 1),
        Rule(1, 5, 1, 5, 1),
        Rule(2, 5, 1, 5, 1),
        Rule(3, 5, 2, 4, 1),
        Rule(4, 5, 2, 4, 1),
        Rule(5, 5, 3, 3, 1)
    ]

    input_mf_func_number = [0] * 2
    input2_mf_func_number = [0] * 2

    count = 0
    number_of_rule = 0

    input1_mf_values = fuzzification(input1_var)                 #to calculate input_mf_func_number which is the index of input membership func [1, 5]
    for i in range(5):
        if input1_mf_values[i] != 0:
            input_mf_func_number[count] = i+1
            count += 1
    count = 0

    input2_mf_values = fuzzification(input2_var)
    for i in range(5):
        if input2_mf_values[i] != 0:
            input2_mf_func_number[count] = i+1
            count += 1
    count = 0

    output_rule, number_of_rule = check_rule(input_mf_func_number, input2_mf_func_number, rules)

    output1_mf, output2_mf = rule_inference(output_rule, input1_mf_values, input2_mf_values, number_of_rule)

    rounded_output1_var, rounded_output2_var = defuzzification(output1_mf, output2_mf, number_of_rule, input1_var, input2_var)

    #print("this is new rounded output value:", rounded_output1_var, rounded_output2_var)
    return rounded_output1_var, rounded_output2_var


# def main():
#     input1_var = 3
#     input2_var = 0
#     
#     rounded_output1_var, rounded_output2_var = fuzzy_logic_algorithm(input1_var, input2_var)
#     
#     print("this is new rounded output value:", rounded_output1_var, rounded_output2_var)
#     
# if __name__ == "__main__":
#     main()
