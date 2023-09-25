
// Set the project name of this folder
// The entire program will compile process all 
// files inside this project declaration
project "Name of project";

// import header files
import library "iostream"

// import packages/namespaces
import System.io;

// @ are pre-processor instructions
@define_entry
func main() {

    System.io.print("Print out to console!");

    // C++ style
    SomeClass someClass = SomeClass(args);

    // Copper Style
    stackClass : SomeClass = SomeClass(args);
    newClass : new SomeClass = SomeClass(args);
    mutClass : mut SomeClass = SomeClass(args);

    delete newClass;
    delete mutClass; // error
}

// This is wrong, you cannot create a file that contains a class declaration
// The class should be in a separate file
class SomeClassInFile {

}

// You can create disposable classes
// in local methods
class SomeClass<E, T, A> {
    extends SuperClass;
    implements interfaces;
    implements interfaces, ...;

    private:

    int number;

    public: 

    // Constructor that flags the compiler that this can throw an error and must be cought
    explicit constructor throws Exception {
        // Initialize all members
        number : param1;
        memberN : paramN;

        // call any in-class method
        method : (number, memberN, paramN, ...);
    }

    // Calls the method when object is about to be destroyed
    destructor {
        method : ();
    }

    public: 

    func method() -> int;
    const func method() -> int;
    final func method() throws Exception -> int;
}

import library "SomeClass";

implement package::root::namespace::SomeClass;

func method() -> int {
    // your code here
}