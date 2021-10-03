#include <iostream>
#include <stdio.h>
#include <cstring>

using namespace std;

string encode(string key, string clear){
    string enc = "";
    char key_c;
    string enc_c;
    int placeholder;
    
    for (int i=0; i < clear.length(); i++){
        key_c = key[i % key.length()];
        placeholder = int(clear[i]) + int(key_c);
        enc_c = (placeholder % 127);
        enc.append(enc_c);
    }
    return enc;
}

string decode(string key, string enc){
    string dec = "";
    char key_c;
    string dec_c;
    int placeholder;
    
    for (int i=0; i < enc.length(); i++){
        key_c = key[i % key.length()];
        placeholder = 127 + int(enc[i]) - int(key_c);
        //cout << placeholder << "\n";
        dec_c = (placeholder % 127);
        dec.append(dec_c);
    }
    return dec;
}



int main()
{
    string key = "qwerty1234"; # KEY 
    string clear = "this is a big string"; # Plaintext
    string result = encode(key, clear);
    cout << result;
    cout << "\n" << decode(key, result);
    return 0;
}
