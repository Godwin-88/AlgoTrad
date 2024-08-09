// OptionData.hpp
//
// Encapsulate option data.
//
// (C) Datasim Education BV 2008-2011

#ifndef OptionData_HPP
#define OptionData_HPP

#include <iostream>
using namespace std;

// Encapsulate all data in one place
struct OptionData
{ // Option data + behaviour

	double K;//Strike Price
	double T;//Expiry Time
	double r;//Interest rate
	double sig;//Volatility

	// Extra data 
	double D;		// dividend
	double beta;	// elasticity factor (Constant Elasticity of Variance (CEV)  model)
	
	int type;		// 1 == call, -1 == put

};

void print (OptionData data) // Call by value
{ //his function prints the contents of an OptionData struct. It takes the struct as a parameter by value, meaning a copy of the struct is passed to the function.
	cout << "Strike: " << data.K << endl;
	cout << "Expiry: " << data.T << endl;
	cout << "Interest: " << data.r << endl;
	cout << "Volatility: " << data.sig << endl;
	cout << "Dividend: " << data.D << endl;
	cout << "Elasticity factor (beta): " << data.beta << endl;
	cout << "Call +1 or Put -1: " << data.type << endl;
}

void print2 (struct OptionData* data) // Call by value
{ //This function prints only some of the contents of an OptionData struct.
// It takes a pointer to the struct as a parameter, allowing it to directly access the original struct rather than a copy.
	cout << "Strike: " << data->K << endl;
	cout << "Expiry: " << data->T << endl;
/*	cout << "Interest: " << data.r << endl;
	cout << "Volatility: " << data.sig << endl;
	cout << "Dividend: " << data.D << endl;
	cout << "Elasticity factor (beta): " << data.beta << endl;
	cout << "Call +1 or Put -1: " << data.type << endl;*/
}



#endif