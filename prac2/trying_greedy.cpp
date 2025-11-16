#include <iostream>
#include <set>
#include <vector>
#include <fstream>
#include <unordered_set>


using namespace std;

void read_from_file(string filename, int& n, int& m, vector<pair<int,int>>& edges){
    ifstream file(filename);
    if(file.is_open()){
        file >> n >> m;
        edges.resize(m);
        for(int i=0; i<m; i++){
            file >> edges[i].first >> edges[i].second;
        }
    }
}

unordered_set<int> vertex_cover_greedy(vector<pair<int,int>>& edges){
    unordered_set<int> vertex_cover;
    for(auto& edge : edges){
        int u = edge.first;
        int v = edge.second;
        if(vertex_cover.find(u) == vertex_cover.end() && vertex_cover.find(v) == vertex_cover.end()){
            vertex_cover.insert(u);
            vertex_cover.insert(v);
        }
    }

    return vertex_cover;
}

int main(){
    int n = 0;
    int m = 0;
    vector<pair<int,int>> edges;

    read_from_file("input.txt",n, m, edges);
    unordered_set vc = vertex_cover_greedy(edges);
    cout << "\nVertex Cover : ";
    for(int value : vc){
        cout << value << " ";
    }

    return 0;
}