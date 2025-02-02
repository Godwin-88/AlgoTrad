//
//  TestGenericInequalities.cpp
//  TestGenericInequalities
//
//  Main program (Console-based) to test Max and Min functions.
//
//  Created by Changheng Chen on 1/21/17.
//  Copyright © 2017 Changheng Chen. All rights reserved.
//

#include <iostream>   // Console input and output
#include <string>     
using namespace std;

#include "GenericInequalities.cpp" // Needed because it is templated

int main()
{
    // Prompt the user for input. Consoel output (cout) and input (cin)
    // int d1, d2;
    // double d1, d2;
    string d1, d2;    // IT WORKS!!!???
    cout << "Give the first number: " ;
    cin >> d1;
    cout << "Give the second number: ";
    cin >> d2;
    
    char c; // Character type
    cout << "Which function a) Max() or b) Min()? ";
    cin >> c;
    
    if (c == 'a')
    {
        //cout << "Max value is: " << Max<int>(d1, d2) << endl;
        cout << "Max value is: " << Max<string>(d1, d2) << endl;
    }
    else
    {
        //cout << "Min value is: " << Min<int>(d1, d2) << endl;
        cout << "Min value is: " << Min<string>(d1, d2) << endl;
    }
    
    long dA = 12334; long dB = 2; long dC = -3;
    cout << "\n\nMax and min of three numbers: " << endl;
    cout << "Max value is: " << Max<long>(dA, dB, dC) << endl;
    cout << "Min value is: " << Min<long>(dA, dB, dC) << endl;
    
    return 0;
}
