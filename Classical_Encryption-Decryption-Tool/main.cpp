#include <iostream>
#include <string>
#include "encryption.h"
using namespace std;
int main() 
{
 string filename;
 char mode;

 cout << "Enter the filename: ";

 getline(cin >> ws, filename);

 cout << "Encrypt (e) or Decrypt (d)?: ";
 cin >> mode;

 if(mode =='e' || mode =='E'){
	if (encryptFile(filename, true)){
		cout << "Encryption completed successfully" << endl;
	}
	else{
		cerr << "Error: Unable to perform encryption" << endl;
	}	
 }
 else if (mode == 'd' || mode == 'D'){
 	if (encryptFile(filename, false)){
		cout << "Decryption completed successfully" << endl;
	}
	else {
		cerr << "Error: Unable to perform decryption" << endl;
	}
 }
 else {
	cerr << "Error: Invalid Input, please try again! Use 'e' for encryption or 'd' for decryption.\n" << endl;
}
return 0;
 
}
