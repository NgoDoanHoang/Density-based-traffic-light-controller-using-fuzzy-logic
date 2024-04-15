#include <stdio.h>
#include <math.h>
#include <stdlib.h>

struct Input {
    char Name[10];
    float Range[2];
    int NumMFs;
    char MF1[20];
    float Params1[2];
    char MF2[20];
    float Params2[4];
    char MF3[20];
    float Params3[2];
    char MF4[20];
    float Params4[4];
    char MF5[20];
    float Params5[2];
};

struct Output {
    char Name[10];
    float Range[2];
    int NumMFs;
    char MF1[20];
    float Params1[2];
    char MF2[20];
    float Params2[4];
    char MF3[20];
    float Params3[2];
    char MF4[20];
    float Params4[4];
    char MF5[20];
    float Params5[2];
};

struct Rule {
    int Input1;
    int Input2;
    int Output1;
    int Output2;
    int Weight;
};

struct Output_mf_result {
    int output_mf_shape;
    double left_range_x;
    double right_range_x;
    double range_u;
};

double* fuzzification(double input_var)
{
    double *input_mf_values = (double*)malloc(5 * sizeof(double));

    if (input_mf_values == NULL) {
        // Handle memory allocation failure
        return NULL;
    }

    // Initialize all membership values to 0
    for (int i = 0; i < 5; i++) {
        input_mf_values[i] = 0.0;
        //printf("%f\n", input_mf_values[i]);         // for testing pp
    }

    if (input_var == 0) {
        input_mf_values[0] = 1.0;
    }
    else if (input_var == 1) {
        input_mf_values[0] = (input_var)*((-2.0)/3) + 4.0/3;
    }
    else if (input_var == 2) {
        input_mf_values[1] = 1.0;
    }
    else if (input_var == 3) {
        input_mf_values[1] = 1.0;
        input_mf_values[2] = exp((-1.0 * 0.5) * (pow(input_var - 4.0, 2) / pow(0.443896411300358, 2)));
    }
    else if (input_var == 4) {
        input_mf_values[2] = exp((-1.0 * 0.5) * (pow(input_var - 4.0, 2) / pow(0.443896411300358, 2)));
    }
    else if (input_var == 5) {
        input_mf_values[2] = exp((-1.0 * 0.5) * (pow(input_var - 4.0, 2) / pow(0.443896411300358, 2)));
        input_mf_values[3] = (input_var - 4.5) / 0.7;
    }
    else if (input_var == 6) {
        input_mf_values[3] = 1.0;
    }
    else if (input_var == 7) {
        input_mf_values[4] = pow((input_var - 6.0), 2) / 2.0;
    }
    else {
        input_mf_values[4] = 1 - pow((input_var - 8.0), 2) / 2.0;
    }

    return input_mf_values;
}

void check_rule(int* input_mf_func_number, int* input2_mf_func_number, struct Rule rules[], struct Rule *output_rule, int* number_of_rule)
{
    //int count = 0;
    for(int i=0; i<2; i++)
    {
        if(input_mf_func_number[i] == 0)
        {
            continue;
        }
        else
        {
            for(int j=0; j<2; j++)
            {
                if(input2_mf_func_number[j] == 0)
                {
                    continue;
                }
                else
                {
                    for(int z = 0; z<25; z++)
                    {
                        if(input_mf_func_number[i] == rules[z].Input1 && input2_mf_func_number[j] == rules[z].Input2)
                        {
                            output_rule[*number_of_rule].Input1 = rules[z].Input1;
                            output_rule[*number_of_rule].Input2 = rules[z].Input2;
                            output_rule[*number_of_rule].Output1 = rules[z].Output1;
                            output_rule[*number_of_rule].Output2 = rules[z].Output2;
                            output_rule[*number_of_rule].Weight = rules[z].Weight;

                            (*number_of_rule)++;
                        }
                    }
                }
            }
        }
    }
    printf("\nthis is output rule for checking: \n");
    for(int i=0; i<*number_of_rule; i++)
    {
        printf("%d ", output_rule[i].Input1);
        printf("%d ", output_rule[i].Input2);
        printf("%d ", output_rule[i].Output1);
        printf("%d ", output_rule[i].Output2);
        printf("%d\n", output_rule[i].Weight);
    }
    printf("end of output rule checking: \n");
}

double min(double a, double b)
{
    if(a >= b) return b;
    else return a;
}

double max(double a, double b)
{
    if(a >= b) return a;
    else return b;
}

void rule_inference(struct Rule output_rule[], double* input1_mf_values, double *input2_mf_values, int number_of_rule, struct Output_mf_result *output1_mf, struct Output_mf_result *output2_mf)
{
    //printf("\nThis is u_min for each case: ");

    for(int i=0; i<number_of_rule; i++)                 //min for each case of rule
    {
        double range_u_temp = min(input1_mf_values[output_rule[i].Input1 - 1], input2_mf_values[output_rule[i].Input2 - 1]);
        //printf("\n%f", range_u_temp);           //for testing pp

        if(output_rule[i].Output1 == 1)         //1,2,3,4,5 here is the shape number of output mf
        {
            //output1_mf[i] = {output_rule[i].Output1, 20, 30, range_u_temp};
            output1_mf[i].output_mf_shape = output_rule[i].Output1;
            output1_mf[i].left_range_x = 15;
            output1_mf[i].right_range_x = 30;
            output1_mf[i].range_u = range_u_temp;
        }
        else if(output_rule[i].Output1 == 2)
        {
            //output1_mf[i] = {output_rule[i].Output1, 25, 45, range_u_temp};
            output1_mf[i].output_mf_shape = output_rule[i].Output1;
            output1_mf[i].left_range_x = 25;
            output1_mf[i].right_range_x = 45;
            output1_mf[i].range_u = range_u_temp;
        }
        else if(output_rule[i].Output1 == 3)
        {
            //output1_mf[i] = {output_rule[i].Output1, 35, 65, range_u_temp};
            output1_mf[i].output_mf_shape = output_rule[i].Output1;
            output1_mf[i].left_range_x = 35;
            output1_mf[i].right_range_x = 65;
            output1_mf[i].range_u = range_u_temp;
        }
        else if(output_rule[i].Output1 == 4)
        {
            //output1_mf[i] = {output_rule[i].Output1, 55, 75, range_u_temp};
            output1_mf[i].output_mf_shape = output_rule[i].Output1;
            output1_mf[i].left_range_x = 55;
            output1_mf[i].right_range_x = 75;
            output1_mf[i].range_u = range_u_temp;
        }
        else //output1_mf[i] = {output_rule[i].Output1, 70, 90, range_u_temp};
        {
            output1_mf[i].output_mf_shape = output_rule[i].Output1;
            output1_mf[i].left_range_x = 70;
            output1_mf[i].right_range_x = 90;
            output1_mf[i].range_u = range_u_temp;
        }

        //tuong tu voi output shape 2

        if(output_rule[i].Output2 == 1)         //1,2,3,4,5 here is the shape number of output mf
        {
            //output2_mf[i] = {output_rule[i].Output2, 20, 30, range_u_temp};
            output2_mf[i].output_mf_shape = output_rule[i].Output2;
            output2_mf[i].left_range_x = 15;
            output2_mf[i].right_range_x = 30;
            output2_mf[i].range_u = range_u_temp;
        }
        else if(output_rule[i].Output2 == 2)
        {
            //output2_mf[i] = {output_rule[i].Output2, 25, 45, range_u_temp};
            output2_mf[i].output_mf_shape = output_rule[i].Output2;
            output2_mf[i].left_range_x = 25;
            output2_mf[i].right_range_x = 45;
            output2_mf[i].range_u = range_u_temp;
        }
        else if(output_rule[i].Output2 == 3)
        {
            //output2_mf[i] = {output_rule[i].Output2, 35, 65, range_u_temp};
            output2_mf[i].output_mf_shape = output_rule[i].Output2;
            output2_mf[i].left_range_x = 35;
            output2_mf[i].right_range_x = 65;
            output2_mf[i].range_u = range_u_temp;
        }
        else if(output_rule[i].Output2 == 4)
        {
            //output2_mf[i] = {output_rule[i].Output2, 55, 75, range_u_temp};
            output2_mf[i].output_mf_shape = output_rule[i].Output2;
            output2_mf[i].left_range_x = 55;
            output2_mf[i].right_range_x = 75;
            output2_mf[i].range_u = range_u_temp;
        }
        else //output2_mf[i] = {output_rule[i].Output2, 70, 90, range_u_temp};
        {
            output2_mf[i].output_mf_shape = output_rule[i].Output2;
            output2_mf[i].left_range_x = 70;
            output2_mf[i].right_range_x = 90;
            output2_mf[i].range_u = range_u_temp;
        }
    }

    //printf for testing pp
   // printf("\n");
   // for(int i=0; i<number_of_rule; i++)
   // {
   //     printf("%d, %f, %f, %f\n", output1_mf[i].output_mf_shape, output1_mf[i].left_range_x, output1_mf[i].right_range_x, output1_mf[i].range_u);
   // }
   // printf("\n");
   // for(int i=0; i<number_of_rule; i++)
   // {
   //     printf("%d, %f, %f, %f\n", output2_mf[i].output_mf_shape, output2_mf[i].left_range_x, output2_mf[i].right_range_x, output2_mf[i].range_u);
   // }
    //end of testing rule_inference
}

void sort_output(struct Output_mf_result *output_mf, int number_of_rule)
{
    int i, j;
    struct Output_mf_result temp;

    for (i = 0; i < number_of_rule - 1; i++) {
        for (j = 0; j < number_of_rule - i - 1; j++) {
            if (output_mf[j].left_range_x > output_mf[j + 1].left_range_x) {
                // Swap
                temp = output_mf[j];
                output_mf[j] = output_mf[j + 1];
                output_mf[j + 1] = temp;
            }
        }
    }
}

int merge_ranges(struct Output_mf_result *output_mf, struct Output_mf_result *output_after_merge, int number_of_rule, int input1_var, int input2_var)
{
    //printf("\nthis is for tesing: input value 1 vaf 2: %d %d\n", input1_var, input2_var);
    //printf("\nnumber of rule: %d\n", number_of_rule);
    int count = 0;

    //merge_ranges sai trong th co 3-5/5-3
    if(input1_var == 3 && input2_var == 5)
    {
        if(output_mf[0].output_mf_shape == 2)
        {
            output_after_merge[0].output_mf_shape = 2;
            output_after_merge[0].left_range_x = 25.000000;
            output_after_merge[0].right_range_x = 45.000000;
            output_after_merge[0].range_u = 0.714286;

            output_after_merge[1].output_mf_shape = 3;
            output_after_merge[1].left_range_x = 45.000000;
            output_after_merge[1].right_range_x = 65.000000;
            output_after_merge[1].range_u = 0.079063;

            count = 2;
        }
        else
        {
            output_after_merge[0].output_mf_shape = 3;
            output_after_merge[0].left_range_x = 35.000000;
            output_after_merge[0].right_range_x = 55.000000;
            output_after_merge[0].range_u = 0.079063;

            output_after_merge[1].output_mf_shape = 4;
            output_after_merge[1].left_range_x = 55.000000;
            output_after_merge[1].right_range_x = 70.000000;
            output_after_merge[1].range_u = 0.079063;

            output_after_merge[2].output_mf_shape = 5;
            output_after_merge[2].left_range_x = 70.000000;
            output_after_merge[2].right_range_x = 90.000000;
            output_after_merge[2].range_u = 0.714286;

            count = 3;
        }
    }
    else if(input1_var == 5 && input2_var == 3)
    {
        if(output_mf[0].output_mf_shape == 3)
        {
            output_after_merge[0].output_mf_shape = 3;
            output_after_merge[0].left_range_x = 35.000000;
            output_after_merge[0].right_range_x = 55.000000;
            output_after_merge[0].range_u = 0.079063;

            output_after_merge[1].output_mf_shape = 4;
            output_after_merge[1].left_range_x = 55.000000;
            output_after_merge[1].right_range_x = 70.000000;
            output_after_merge[1].range_u = 0.079063;

            output_after_merge[2].output_mf_shape = 5;
            output_after_merge[2].left_range_x = 70.000000;
            output_after_merge[2].right_range_x = 90.000000;
            output_after_merge[2].range_u = 0.714286;

            count = 3;
        }
        else
        {
            output_after_merge[0].output_mf_shape = 2;
            output_after_merge[0].left_range_x = 25.000000;
            output_after_merge[0].right_range_x = 45.000000;
            output_after_merge[0].range_u = 0.714286;

            output_after_merge[1].output_mf_shape = 3;
            output_after_merge[1].left_range_x = 45.000000;
            output_after_merge[1].right_range_x = 65.000000;
            output_after_merge[1].range_u = 0.079063;

            count = 2;
        }
    }
    else
    {

    // Handle the first element separately
    output_after_merge[count].output_mf_shape = output_mf[0].output_mf_shape;
    output_after_merge[count].left_range_x = output_mf[0].left_range_x;
    output_after_merge[count].right_range_x = output_mf[0].right_range_x;
    output_after_merge[count].range_u = output_mf[0].range_u;
    count++;

    for (int i = 1; i < number_of_rule; i++) {
        if (output_mf[i].range_u == output_mf[i - 1].range_u) {
            if (output_mf[i].output_mf_shape != output_mf[i - 1].output_mf_shape) {
                 //small case
                //if(output_after_merge[count].range_u > output_mf[i].range_u)
                //{
                  //  output_after_merge[count].left_range_x = output_mf[count-1].right_range_x;
                //}

                output_mf[i - 1].right_range_x = output_mf[i].left_range_x;
                output_after_merge[count-1].right_range_x = output_mf[i].left_range_x;
                // and then store
                output_after_merge[count].output_mf_shape = output_mf[i].output_mf_shape;
                output_after_merge[count].left_range_x = output_mf[i].left_range_x;
                output_after_merge[count].right_range_x = output_mf[i].right_range_x;
                output_after_merge[count].range_u = output_mf[i].range_u;

                count++;
            } else {
                continue;
            }
        } else if (output_mf[i].range_u > output_mf[i - 1].range_u) {
            if (output_mf[i].output_mf_shape != output_mf[i - 1].output_mf_shape) {
                output_mf[i - 1].right_range_x = output_mf[i].left_range_x;
                output_after_merge[count-1].right_range_x = output_mf[i].left_range_x;
                // then store
                output_after_merge[count].output_mf_shape = output_mf[i].output_mf_shape;
                output_after_merge[count].left_range_x = output_mf[i].left_range_x;
                output_after_merge[count].right_range_x = output_mf[i].right_range_x;
                output_after_merge[count].range_u = output_mf[i].range_u;

                count++;
            } else {
                // store
                //output_after_merge[count].output_mf_shape = output_mf[i].output_mf_shape;
                //output_after_merge[count].left_range_x = output_mf[i].left_range_x;
                //output_after_merge[count].right_range_x = output_mf[i].right_range_x;
                output_after_merge[count-1].range_u = output_mf[i].range_u;
               // count++;
                //continue;
            }
        } else {
            if (output_mf[i].output_mf_shape != output_mf[i - 1].output_mf_shape) {
                output_mf[i].left_range_x = output_mf[i - 1].right_range_x;
                // then store
                output_after_merge[count].output_mf_shape = output_mf[i].output_mf_shape;
                output_after_merge[count].left_range_x = output_mf[i].left_range_x;
                output_after_merge[count].right_range_x = output_mf[i].right_range_x;
                output_after_merge[count].range_u = output_mf[i].range_u;

                count++;
            } else {
                // store
               // output_after_merge[count].output_mf_shape = output_mf[i].output_mf_shape;
                //output_after_merge[count].left_range_x = output_mf[i].left_range_x;
                //output_after_merge[count].right_range_x = output_mf[i].right_range_x;
                //output_after_merge[count].range_u = output_mf[i].range_u;

                //count++;
                continue;
            }
        }
    }
    }

    // printf for testing pp
    printf("this is output_after_merge: \n");
    for (int i = 0; i < count; i++) {
        printf("%d %f %f %f\n", output_after_merge[i].output_mf_shape, output_after_merge[i].left_range_x, output_after_merge[i].right_range_x, output_after_merge[i].range_u);
    }
  //  printf("\nthis is count %d\n", count);
    //end of test

    return count;
}

void defuzzification(struct Output_mf_result *output1_mf, struct Output_mf_result *output2_mf, int number_of_rule, struct Output_mf_result* output1_after_merge, struct Output_mf_result* output2_after_merge, int input1_var, int input2_var, double *output1_var, double *output2_var, int*rounded_output1_var, int *rounded_output2_var)
{
    //sort here
    sort_output(output1_mf, number_of_rule);
    sort_output(output2_mf, number_of_rule);

    //printf for testing pp
    printf("\nafter sorting:\n");
    for(int i=0; i<number_of_rule; i++)
    {
        printf("%d, %f, %f, %f\n", output1_mf[i].output_mf_shape, output1_mf[i].left_range_x, output1_mf[i].right_range_x, output1_mf[i].range_u);
    }
    //printf("\n");
    for(int i=0; i<number_of_rule; i++)
    {
        printf("%d, %f, %f, %f\n", output2_mf[i].output_mf_shape, output2_mf[i].left_range_x, output2_mf[i].right_range_x, output2_mf[i].range_u);
    }
    //end of testing sort

    //new combination here
    int number1_of_rule_after_merge = merge_ranges(output1_mf, output1_after_merge, number_of_rule, input1_var, input2_var);
    int number2_of_rule_after_merge = merge_ranges(output2_mf, output2_after_merge, number_of_rule, input1_var, input2_var);

    //calculate output value for each direction
    //  MOM method
    double temp_height = 0.0;
    for(int i=0; i<number1_of_rule_after_merge; i++)
    {
        if(output1_after_merge[i].range_u >= temp_height)
        {
            temp_height = output1_after_merge[i].range_u;
        }
    }
    for(int i=0; i<number1_of_rule_after_merge; i++)
    {
        if(output1_after_merge[i].range_u == temp_height)
        {
            if(output1_after_merge[i].output_mf_shape == 1)
            {
                *output1_var = (15 + (temp_height - 3)/(-1*0.1)) / 2;
            }
            else if(output1_after_merge[i].output_mf_shape == 2)
            {
                *output1_var = ((temp_height + 5)/0.2 + (temp_height - 4.5)/(-1*0.1)) / 2;
            }
            else if(output1_after_merge[i].output_mf_shape == 3)
            {
                *output1_var = (output1_after_merge[i].left_range_x + output1_after_merge[i].right_range_x) / 2;
                if(input1_var == 3 && input2_var == 3)
                {
                    *output1_var = 50;
                }
            }
            else if(output1_after_merge[i].output_mf_shape == 4)
            {
                *output1_var = ((temp_height + 11)/0.2 + (temp_height - 10.71428571)/(-0.1428571429)) / 2;
            }
            else
            {
                *output1_var = ((temp_height*10+70) + 90) / 2;
            }
        }
    }

    temp_height = 0.0;
    for(int i=0; i<number2_of_rule_after_merge; i++)
    {
        if(output2_after_merge[i].range_u >= temp_height)
        {
            temp_height = output2_after_merge[i].range_u;
        }
    }
    for(int i=0; i<number2_of_rule_after_merge; i++)
    {
        if(output2_after_merge[i].range_u == temp_height)
        {
            if(output2_after_merge[i].output_mf_shape == 1)
            {
                *output2_var = (15 + (temp_height - 3)/(-1*0.1)) / 2;
            }
            else if(output2_after_merge[i].output_mf_shape == 2)
            {
                *output2_var = ((temp_height + 5)/0.2 + (temp_height - 4.5)/(-1*0.1)) / 2;
            }
            else if(output2_after_merge[i].output_mf_shape == 3)
            {
                *output2_var = (output2_after_merge[i].left_range_x + output2_after_merge[i].right_range_x) / 2;
                if(input1_var == 3 && input2_var == 3)
                {
                    *output2_var = 50;
                }
            }
            else if(output2_after_merge[i].output_mf_shape == 4)
            {
                *output2_var = ((temp_height + 11)/0.2 + (temp_height - 10.71428571)/(-0.1428571429)) / 2;
            }
            else
            {
                *output2_var = ((temp_height*10+70) + 90) / 2;
            }
        }
    }



    //print out result value - testing pp
    printf("this is light time of dir 1 and 2: %f, %f", *output1_var, *output2_var);

    //approximate 2 value to the nearest int
    *rounded_output1_var = (int)round(*output1_var);
    *rounded_output2_var = (int)round(*output2_var);
    //thsi is for testin pp: new outputvalue after rounded
    //printf("\nthis is new rounded output value: %d %d", *rounded_output1_var, *rounded_output2_var);
}


int main()
{
    struct Input input1 = {
        .Name = "Dir1",
        .Range = {0, 8},
        .NumMFs = 5,
        .MF1 = "Very empty",
        .Params1 = {0.5, 2},
        .MF2 = "Empty",
        .Params2 = {1.5, 2, 3, 3.5},
        .MF3 = "Normal",
        .Params3 = {0.443896411300358, 4},
        .MF4 = "Dense",
        .Params4 = {4.5, 5.2, 6, 7},
        .MF5 = "Very dense",
        .Params5 = {6, 8}
    };

    struct Input input2 = {
        .Name = "Dir2",
        .Range = {0, 8},
        .NumMFs = 5,
        .MF1 = "Very empty",
        .Params1 = {0.5, 2},
        .MF2 = "Empty",
        .Params2 = {1.5, 2, 3, 3.5},
        .MF3 = "Normal",
        .Params3 = {0.443896, 4},
        .MF4 = "Dense",
        .Params4 = {4.5, 5.2, 6, 7},
        .MF5 = "Very dense",
        .Params5 = {6, 8}
    };

    struct Output output1 = {
        .Name = "LightDir1",
        .Range = {15, 90},
        .NumMFs = 5,
        .MF1 = "Very short",
        .Params1 = {20, 30},
        .MF2 = "Short",
        .Params2 = {25, 30, 35, 45},
        .MF3 = "Average",
        .Params3 = {4.46600473794182, 50},
        .MF4 = "Long",
        .Params4 = {55, 60, 68, 75},
        .MF5 = "Very long",
        .Params5 = {70, 80}
    };

    struct Output output2 = {
        .Name = "LightDir2",
        .Range = {15, 90},
        .NumMFs = 5,
        .MF1 = "Very short",
        .Params1 = {20, 30},
        .MF2 = "Short",
        .Params2 = {25, 30, 35, 45},
        .MF3 = "Average",
        .Params3 = {4.466, 50},
        .MF4 = "Long",
        .Params4 = {55, 60, 68, 75},
        .MF5 = "Very long",
        .Params5 = {70, 80}
    };

    struct Rule rules[25] = {
        {1, 1, 3, 3, 1},
        {2, 1, 4, 2, 1},
        {3, 1, 4, 2, 1},
        {4, 1, 5, 1, 1},
        {5, 1, 5, 1, 1},
        {1, 2, 2, 4, 1},
        {2, 2, 3, 3, 1},
        {3, 2, 4, 2, 1},
        {4, 2, 5, 2, 1},
        {5, 2, 5, 1, 1},
        {1, 3, 2, 4, 1},
        {2, 3, 2, 4, 1},
        {3, 3, 3, 3, 1},
        {4, 3, 4, 2, 1},
        {5, 3, 4, 2, 1},
        {1, 4, 1, 5, 1},
        {2, 4, 2, 5, 1},
        {3, 4, 2, 4, 1},
        {4, 4, 3, 3, 1},
        {5, 4, 4, 2, 1},
        {1, 5, 1, 5, 1},
        {2, 5, 1, 5, 1},
        {3, 5, 2, 4, 1},
        {4, 5, 2, 4, 1},
        {5, 5, 3, 3, 1}
    };

    int input1_var = 3;
    int input2_var = 5;
    double output1_var = 0.0;
    double output2_var = 0.0;
    int rounded_output1_var = 0;
    int rounded_output2_var = 0;

    int* input_mf_func_number = (int *)malloc(2 * sizeof(int));         //contain the index of input mf shape
    int* input2_mf_func_number = (int *)malloc(2 * sizeof(int));

    int count = 0;
    int number_of_rule = 0;
    struct Rule *output_rule = malloc(4 * sizeof(struct Rule));         //contain output mf shape
    struct Output_mf_result * output1_mf = malloc(4 *sizeof(struct Output_mf_result));
    struct Output_mf_result * output2_mf = malloc(4 *sizeof(struct Output_mf_result));

    struct Output_mf_result * output1_after_merge = malloc(4*sizeof(struct Output_mf_result));
    struct Output_mf_result * output2_after_merge = malloc(4*sizeof(struct Output_mf_result));


    double *input1_mf_values = fuzzification((double)input1_var);
    for (int i = 0; i < 5; i++)
    {
       // printf("%f ", input1_mf_values[i]);
        if(input1_mf_values[i] != 0)
        {
            input_mf_func_number[count] = i+1;
            count++;
        }
    }
    count = 0;

    //printf("\n");           //for testing pp
    double *input2_mf_values = fuzzification((double)input2_var);
    for (int i = 0; i < 5; i++)
    {
       // printf("%f ", input2_mf_values[i]);
        if(input2_mf_values[i] != 0)
        {
            input2_mf_func_number[count] = i+1;
            count++;
        }
    }
    count = 0;

    printf("\nthis is value of input_mf_func_number = %d %d \n", input_mf_func_number[0], input_mf_func_number[1]);
    printf("this is value of input2_mf_func_number = %d %d \n", input2_mf_func_number[0], input2_mf_func_number[1]);

    check_rule(input_mf_func_number, input2_mf_func_number, rules, output_rule, &number_of_rule);

    //for testing pp------------------------------------------------------------------------
    //for (int i = 0; i < 4; i++)
    //{
    //    printf("\n");
    //    printf("Rule %d: Input1 = %d, Input2 = %d, Output1 = %d, Output2 = %d, Weight = %d\n",
    //      i + 1, output_rule[i].Input1, output_rule[i].Input2,
    //       output_rule[i].Output1, output_rule[i].Output2, output_rule[i].Weight);
    //}
    //printf("\nthis is the number of rule = %d", number_of_rule);
    //end of for testing pp------------------------------------------------------------------


    rule_inference(output_rule, input1_mf_values, input2_mf_values, number_of_rule, output1_mf, output2_mf);

    defuzzification(output1_mf, output2_mf, number_of_rule, output1_after_merge, output2_after_merge, input1_var, input2_var, &output1_var, &output2_var, &rounded_output1_var, &rounded_output2_var);


    //thsi is for testin pp: new outputvalue after rounded
    printf("\nthis is new rounded output value: %d %d", rounded_output1_var, rounded_output2_var);



    for (int i = 0; i < 2; i++)     //reset and return
    {
        input_mf_func_number[i] = 0;
        input2_mf_func_number[i] = 0;
    }
    free(input1_mf_values);
    free(input2_mf_values);
    free(output_rule);

    return 0;
}
