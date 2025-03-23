#ifndef MAINHEADER_H
#define MAINHEADER_H
#include <algorithm>
#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <stdexcept>
#include <cassert>
using namespace std ;
 
class Book {
public:
    Book(const std::string& title, const std::string& author, const std::string& ISBN, int year, bool isAvailable);
    std::string getTitle() const;
    std::string getAuthor() const;
    std::string getISBN() const;
    int getYear() const;
    bool getAvailability() const;
    void setAvailability(bool available);
    void displayBook() const;

private:
    std::string title;
    std::string author;
    std::string ISBN;
    int year;
    bool isAvailable;
};

class Library {
public:
    void addBook(const Book& book);
    void removeBook(const std::string& ISBN);
    void searchBookByTitle(const std::string& title) const;
    void displayBooks() const;
    Book* findBookByISBN(const std::string& ISBN);

private:
    std::vector<Book> books;
};

void loadBooksFromFile(Library& library, const std::string& filename);
void saveBooksToFile(const Library& library, const std::string& filename);
void checkoutBook(Library& library, const std::string& ISBN);
void returnBook(Library& library, const std::string& ISBN);


const int MAX_SIZE = 100;

struct Node {
    int key;
    int left;
    int right;
    int height;

    Node() : key(0), left(-1), right(-1), height(1) {}
};

class AVLTree {
private:
    Node nodes[MAX_SIZE];
    int root;
    int freeIndex;

public:
    AVLTree() {
        root = -1; // Initially, the tree is empty
        freeIndex = 0;
    }

    // Helper function to get a new node index
    int getNewNode(int key) {
        if (freeIndex >= MAX_SIZE) {
            cout << "Tree is full!" << endl;
            return -1;
        }

        int index = freeIndex++;
        nodes[index].key = key;
        nodes[index].left = -1;
        nodes[index].right = -1;
        nodes[index].height = 1;
        return index;
    }

    // Get the height of a node
    int height(int index) {
        if (index == -1) return 0;
        return nodes[index].height;
    }

    // Get the balance factor of a node
    int getBalance(int index) {
        if (index == -1) return 0;
        return height(nodes[index].left) - height(nodes[index].right);
    }

    // Left rotate the subtree rooted with node
    int rotateLeft(int z) {
        int y = nodes[z].right;
        int T2 = nodes[y].left;

        // Perform rotation
        nodes[y].left = z;
        nodes[z].right = T2;

        // Update heights
        nodes[z].height = max(height(nodes[z].left), height(nodes[z].right)) + 1;
        nodes[y].height = max(height(nodes[y].left), height(nodes[y].right)) + 1;

        return y;  // Return the new root
    }

    // Right rotate the subtree rooted with node
    int rotateRight(int y) {
        int x = nodes[y].left;
        int T2 = nodes[x].right;

        // Perform rotation
        nodes[x].right = y;
        nodes[y].left = T2;

        // Update heights
        nodes[y].height = max(height(nodes[y].left), height(nodes[y].right)) + 1;
        nodes[x].height = max(height(nodes[x].left), height(nodes[x].right)) + 1;

        return x;  // Return the new root
    }

    // Insert a new key into the tree
    int insert(int index, int key) {
        if (index == -1) return getNewNode(key);

        if (key < nodes[index].key) {
            nodes[index].left = insert(nodes[index].left, key);
        } else {
            nodes[index].right = insert(nodes[index].right, key);
        }

        // Update height of this ancestor node
        nodes[index].height = max(height(nodes[index].left), height(nodes[index].right)) + 1;

        // Get the balance factor and balance the tree
        int balance = getBalance(index);

        // Left heavy (Right rotation)
        if (balance > 1 && key < nodes[nodes[index].left].key) {
            return rotateRight(index);
        }

        // Right heavy (Left rotation)
        if (balance < -1 && key > nodes[nodes[index].right].key) {
            return rotateLeft(index);
        }

        // Left-right heavy (Left-right rotation)
        if (balance > 1 && key > nodes[nodes[index].left].key) {
            nodes[index].left = rotateLeft(nodes[index].left);
            return rotateRight(index);
        }

        // Right-left heavy (Right-left rotation)
        if (balance < -1 && key < nodes[nodes[index].right].key) {
            nodes[index].right = rotateRight(nodes[index].right);
            return rotateLeft(index);
        }

        return index;  // Return the unchanged node
    }

    // Public insert method to insert a new key
    void insert(int key) {
        root = insert(root, key);
    }

    // Pre-order traversal
    void preOrder(int index) {
        if (index == -1) return;
        cout << nodes[index].key << " ";
        preOrder(nodes[index].left);
        preOrder(nodes[index].right);
    }

    void printPreOrder() {
        preOrder(root);
        cout << endl;
    }
};

class ArenaAllocator {
    private:
        char* arena;      // Pointer to the large pre-allocated memory block
        size_t arena_size; // Total size of the arena
        size_t offset;    // Offset that keeps track of the next available memory position
    
    public:
        // Constructor to initialize the arena with a given size
        ArenaAllocator(size_t size) : arena_size(size), offset(0) {
            arena = new char[arena_size];
        }
    
        // Destructor to free the arena
        ~ArenaAllocator() {
            delete[] arena;
        }
    
        // Allocate memory from the arena
        void* allocate(size_t size) {
            if (offset + size > arena_size) {
                std::cerr << "Arena memory overflow!" << std::endl;
                return nullptr;
            }
            void* ptr = arena + offset;
            offset += size;  // Move the offset forward
            return ptr;
        }
    
        // Reset the arena, effectively freeing all allocations
        void reset() {
            offset = 0; // Reset the offset to reuse the arena
        }
    };
    
    class ExampleObject {
    public:
        int x;
        double y;
    
        ExampleObject(int x, double y) : x(x), y(y) {}
    
        void print() {
            std::cout << "ExampleObject(x: " << x << ", y: " << y << ")" << std::endl;
        }
    };
    template<typename T>
    class RingBuffer {
    private:
        T* buffer;         // Pointer to the buffer array
        size_t capacity;   // Maximum capacity of the buffer
        size_t size;       // Current number of elements in the buffer
        size_t front;      // Pointer to the front of the buffer
        size_t back;       // Pointer to the back of the buffer
    
    public:
        // Constructor to initialize the ring buffer with a given size
        RingBuffer(size_t capacity) 
            : capacity(capacity), size(0), front(0), back(0) {
            buffer = new T[capacity];
        }
    
        // Destructor to free the allocated memory
        ~RingBuffer() {
            delete[] buffer;
        }
    
        // Push an item to the buffer (write operation)
        void push(const T& item) {
            if (isFull()) {
                throw std::overflow_error("Ring buffer is full");
            }
            buffer[back] = item;  // Place the item at the back
            back = (back + 1) % capacity; // Move the back pointer in a circular fashion
            size++;
        }
    
        // Pop an item from the buffer (read operation)
        T pop() {
            if (isEmpty()) {
                throw std::underflow_error("Ring buffer is empty");
            }
            T item = buffer[front]; // Get the item at the front
            front = (front + 1) % capacity; // Move the front pointer in a circular fashion
            size--;
            return item;
        }
    
        // Peek at the next item to be popped (without removing it)
        T peek() const {
            if (isEmpty()) {
                throw std::underflow_error("Ring buffer is empty");
            }
            return buffer[front];
        }
    
        // Check if the buffer is full
        bool isFull() const {
            return size == capacity;
        }
    
        // Check if the buffer is empty
        bool isEmpty() const {
            return size == 0;
        }
    
        // Get the current number of elements in the buffer
        size_t getSize() const {
            return size;
        }
    };
    



#endif 
