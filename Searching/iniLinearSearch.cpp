#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <time.h>
using namespace std;

int main() {
    string line;
     //getting the time for linear search.
    ifstream myfile("/Users/Janjua/Desktop/BSCS/3rd Semester/DSA/Project/simplewiki.xml");
    if(myfile.is_open()){
        cout << "File is read!" << endl;
        clock_t start = clock();
        while ( getline (myfile,line)){
            // converting line to c-style strings to compare.
            if(strcmp(line.c_str(), "August") == 0){ // Checks if the word is in the file, if so, it prints it.
                cout << line << endl;
                clock_t end = clock();
                double time = (double) (end-start) / CLOCKS_PER_SEC * 1000.0;
                cout << "The time taken is: " << time*0.001 << " secs" << endl;
                exit(0);
            }
        }

    }else{cout << "Not read!";}

    return 0;
}
