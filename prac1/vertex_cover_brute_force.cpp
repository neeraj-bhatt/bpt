#include <iostream>
#include <vector>
#include <set>
#include <ctime>
#include <iterator>
#include <fstream>
#include <algorithm>
#include <numeric>

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
    ofstream outfile("output.text");
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
    cout << "Results written to ouput file" << endl;
}

// Function to find the minimum vertex cover using brute force
void brute_force_vertex_cover(int n, const vector<pair<int, int>>& edges) {
    // start measuring time
    clock_t start_time = clock();
    
    int min_cover_size = n;  // The maximum size is n
    set<int> best_cover;

    // Iterate through all possible subsets of vertices
    for (int size = 1; size <= n; size++) {
        vector<int> vertices(n);
        iota(vertices.begin(), vertices.end(), 0);  // Generate a list of vertices [0, 1, ..., n-1]

        do {
            set<int> current_cover;
            for (int i = 0; i < size; i++) {
                current_cover.insert(vertices[i]);
            }

            // Check if current_cover is a vertex cover
            if (is_vertex_cover(current_cover, edges)) {
                if (current_cover.size() < min_cover_size) {
                    min_cover_size = current_cover.size();
                    best_cover = current_cover;
                }
                break; // No need to check larger subsets for this size
            }

        } while (next_permutation(vertices.begin(), vertices.end()));

        if (min_cover_size == size) break;  // If we found the smallest vertex cover, stop
    }
    
    clock_t end_time = clock();

    double time_taken = double(end_time - start_time) / CLOCKS_PER_SEC;
    
    // Output the result
    generate_output_file(min_cover_size, best_cover, time_taken);
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
    
    read_graph_from_file(filename, n, m, edges);

    // Find the minimum vertex cover using brute force
    brute_force_vertex_cover(n, edges);
    
    return 0;
}
