#include <iostream>
#include <vector>
#include <unordered_set>
#include <fstream>
#include <ctime>

using namespace std;

// Function to write result in ouput.txt file
void generate_output_file(int &cover_size, unordered_set<int> best_cover, double time_taken){
    cout << "Generating Output file." << endl;
    ofstream outfile("output.txt");
    if (!outfile.is_open()) {
        cerr << "Error: Could not open output.txt for writing.\n";
    }
    outfile << "Vertex cover size: " << cover_size << endl;
    outfile << "Vertex cover (at most 2 times of optimal): ";
    for (int vertex : best_cover) {
        outfile << vertex << " ";
    }
    outfile << endl;
    outfile << "Running time: " << time_taken << " seconds" << endl;
    outfile.close();
    cout << "Results written to ouput.txt." << endl;
}

void vertexCover(vector<pair<int,int>> edges) {

    clock_t start_time = clock();

    unordered_set<int> vertex_cover; // The set to store the vertex cover
    unordered_set<int> covered; // (stores vertices added to vertex_cover)To mark visited edges

    // Iterate over all the edges
    for (auto& edge : edges) {
        int u = edge.first;
        int v = edge.second;

        // If neither of u and v is present in covered vertices set
        if(covered.find(u) == covered.end() && covered.find(v) == covered.end()){
            // Add both u and v to vertex cover
            vertex_cover.insert(u);
            vertex_cover.insert(v);

            // Add both vertices to covered to mark them as covered
            covered.insert(u);
            covered.insert(v);
        }
    }
    clock_t end_time = clock();
    int cover_size = vertex_cover.size();
    double time_taken = double(end_time - start_time) / CLOCKS_PER_SEC;


    generate_output_file(cover_size, vertex_cover, time_taken);
}

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


int main(){
    string filename = "input.txt";

    int n, m;
    vector<pair<int,int>> edges;

    cout << "Generating random edges using python..." << endl;
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

    vertexCover(edges);

    cout << "\nDrawing Vertex Cover Graph..." << endl;
    result = system("python3 graph.py vc input.txt output.txt");
    if(result != 0){
        cerr << "error running vertex cover graph Python script" << endl;
        return 1;
    }

    return 0;
}