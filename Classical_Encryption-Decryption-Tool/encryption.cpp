#include "encryption.h"
#include <fstream>
#include <cctype>
using namespace std;

bool performCeaserCipher(string & content, bool encrypt){
 int shift = encrypt ? 3 : -3;

 for (char & ch: content){
  if(isalpha(ch)){
	  char base = isupper(ch) ? 'A' : 'a';
	  ch = static_cast<char>((ch - base + shift + 26) % 26 + base);
  }
 }
 return true;
}









bool encryptFile(const string & filename, bool encrypt)
{

	//OPEN THE CONTENT OF THE FILE
	ifstream inputFile(filename);
	if (!inputFile){
		return false;
	}

	//READ THE CONTENT OF THE FILE
	string content((istreambuf_iterator<char>(inputFile)), {});;

	inputFile.close();

	if(performCeaserCipher(content, encrypt)){
		//Create an output file and writing the modified content
		ofstream outputFile(encrypt ? "encrypted_" + filename : "decrypted_" + filename);
		if (!outputFile){
			return false;
		}

		outputFile << content;

		outputFile.close();
		return true;
	}	 
}
