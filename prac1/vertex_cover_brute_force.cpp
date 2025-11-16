// took the help of chatgpt for various built-in methods
#include <iostream>
#include <vector>
#include <set>
#include <ctime>
#include <fstream>
#include <algorithm>
#include <cstdlib> // for system calls

using namespace std;

// Function to check if a given set of vertices is a vertex cover
bool is_vertex_cover(const set<int>& vertex_cover, const vector<pair<int, int>>& edges) {
    for (const auto& edge : edges) {
        if (vertex_cover.find(edge.first) == vertex_cover.end() && vertex_cover.find(edge.second) == vertex_cover.end()) {
            return false;  // This edge is not covered
        }
    }
    return true;
}

// Function to write result in ouput.txt file
void generate_output_file(int &min_cover_size, set<int> best_cover, double time_taken){
    cout << "Generating Output file." << endl;
    ofstream outfile("output.txt");
    if (!outfile.is_open()) {
        cerr << "Error: Could not open output.txt for writing.\n";
    }
    outfile << "Minimum vertex cover size: " << min_cover_size << endl;
    outfile << "Best vertex cover: ";
    for (int vertex : best_cover) {
        outfile << vertex << " ";
    }
    outfile << endl;
    outfile << "Running time: " << time_taken << " seconds" << endl;
    outfile.close();
    cout << "Results written to ouput.txt." << endl;
}

// used chatgpt to generate this method
// Helper function to generate the next combination
bool next_combination(vector<int>& combination, int n) {
    int size = combination.size();
    int i = size - 1;
    while (i >= 0 && combination[i] == n - size + i) {
        i--;
    }
    if (i < 0) return false;  // No more combinations

    combination[i]++;
    for (int j = i + 1; j < size; j++) {
        combination[j] = combination[j - 1] + 1;
    }
    return true;
}

// used chatgpt here for various built-in method
// Function to find the minimum vertex cover using brute force
void brute_force_vertex_cover(int n, const vector<pair<int, int>>& edges) {
    cout << "\nCalculating Vertex Cover..." << endl;
    // start measuring time
    clock_t start_time = clock();
    
    int min_cover_size = n;  // The maximum size is n
    set<int> vertex_cover;

    vector<int> vertices(n);
    for(int i=0; i<n; i++)
        vertices[i] = i+1;

    // Iterate through all possible subsets of vertices
    for (int size = 1; size <= n; size++) {
        bool found_cover = false;

        vector<int> combination(size);
        for(int i=0; i<size; i++)
            combination[i] = i;
    
        do {
            set<int> current_combination;
            for (int i = 0; i < size; i++) {
                current_combination.insert(vertices[combination[i]]);
            }

            if (is_vertex_cover(current_combination, edges)) {
                min_cover_size = current_combination.size();
                vertex_cover = current_combination;
                found_cover = true;
                break;  // No need to check larger subsets
            }

        } while (next_combination(combination, n));

        if (found_cover) break;  // If we found the smallest vertex cover, stop
    }
    
    clock_t end_time = clock();

    double time_taken = double(end_time - start_time) / CLOCKS_PER_SEC;
    
    // Output the result
    generate_output_file(min_cover_size, vertex_cover, time_taken);
}

// Function to read the graph from a file
void read_graph_from_file(const string& filename, int& n, int& m, vector<pair<int, int>>& edges) {
    ifstream file(filename);
    if (file.is_open()) {
        file >> n >> m;
        edges.resize(m);
        for (int i = 0; i < m; i++) {
            file >> edges[i].first >> edges[i].second;
        }
    } else {
        cerr << "Failed to open the file." << endl;
    }
}


int main() {
    string filename = "input.txt";  // The input file containing the graph data

    // Read the graph from the file
    int n, m;
    vector<pair<int, int>> edges;

    cout << "Generating ramdom Edges using Python..." << endl;
    int result = system("python3 graph.py generate input.txt");
    if(result != 0){
        cerr << "error running graph generator Python script" << endl;
        return 1;
    }
    cout << "Random Edges generated." << endl;

    cout << "\nDrawing Graph..." << endl;;
    result = system("python3 graph.py draw input.txt");
    if(result != 0){
        cerr << "error running draw graph Python script" << endl;
        return 1;
    }
    cout << "Graph Drawn." << endl;
    
    read_graph_from_file(filename, n, m, edges);

    // Find the minimum vertex cover using brute force
    brute_force_vertex_cover(n, edges);

    cout << "\nDrawing Vertex Cover Graph..." << endl;
    result = system("python3 graph.py vc input.txt output.txt");
    if(result != 0){
        cerr << "error running vertex cover graph Python script" << endl;
        return 1;
    }

    return 0;
}
