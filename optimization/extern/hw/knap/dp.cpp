#include <iostream>
#include <fstream>
#include <vector>

using namespace std;
ofstream output("sols/dp.out");


long long items[10050][2];
void solve(string path) {
    ifstream input(path);
    long long N, W;
    input>> N>>W;
    cout << "started "<<path<<endl;
    cout << "    time: "<<W<< " "<<N*W/1e8<<endl;
    cout << "    score: ";
    for (int i = 0; i< N; i++) {
        input >> items[i][0] >> items[i][1];
    }
    vector<vector<long long> > memo = vector<vector<long long> >(W+1, vector<long long>(2));
    for (int i = 0; i <= W; i++) memo[i][1] = 0;
    long long best =0;
    for (int i = 0; i < N; i++) {
        for (int  w = 0; w <= W; w++) {
            memo[w][i&1]=memo[w][1-(i&1)];
            if (w+items[i][1] <=W) {
                memo[w][i&1]=max(memo[w][i&1], memo[w+items[i][1]][1-(i&1)]+items[i][0]);
            }
            best=max(best, memo[w][i&1]);
        }
    }
    output<<path<< " "<< memo[0][W&1]<<"\n";
    cout << best<<endl;
}

int main () {
    string cases[] = {"ks_4_0",
        "ks_19_0",
        "ks_30_0",
        "ks_40_0",
        "ks_45_0",
        "ks_50_0",
        "ks_50_1",
        "ks_60_0",
        "ks_82_0",
        "ks_100_0",
        "ks_100_1",
        "ks_106_0",
        "ks_200_0",
        "ks_200_1",
        "ks_300_0",
        "ks_400_0",
        "ks_500_0",
        "ks_1000_0",
        "ks_10000_0"};
    for (string cased: cases)
        solve(cased);
}
