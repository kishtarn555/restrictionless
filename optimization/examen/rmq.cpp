#include<iostream>
#include<vector>
#include<algorithm>
#include<utility>
#include<set>
#include<queue>
#include<string>

using namespace std;
using ll = long long;

struct item {
    ll p, w;
    int pos;
    bool operator <(const item & other) const {
        return w < other.w;
    }
};
int N, W;
vector<item> items;

struct data {
    ll totalScore, totalWeight;
    double fitness;
};

using pli = pair<ll, int>;
pli segmenttree[100050];
void build() {
    for (int p = 0; p<N; p++) segmenttree[N+p] =  pli(items[p].p, p);
    for (int p = N-1; p>=1; p--) {
        segmenttree[p] = max(segmenttree[(p<<1)],segmenttree[(p<<1)|1]);
    }
}

void update(int pos, ll value) {
    int p = pos+N;
    segmenttree[p].first=value;
    while(p>>=1) segmenttree[p] = max(segmenttree[(p<<1)],segmenttree[(p<<1)|1]);
}

pli findCandidate(int l, int r) {
    pli res = pli(-1e18, -1e18);
    for (l += N, r += N; l < r; l >>= 1, r >>= 1) {
        if (l&1) res = max(res,segmenttree[l++]);
        if (r&1) res = max(res, segmenttree[--r]);
    }
  return res;
}

deque<int> tabu;

vector<int> solution(N, 0);
void addToSolution(int pos, int capacity, set<item> & available) {
    update(pos, -1e18);
    tabu.push_back(pos);
    available.erase(items[pos]);
    if (tabu.size() > capacity) {
            int fit = tabu.front();
            if (solution[fit]) {
                available.insert(items[fit]);
            }
            tabu.pop_front();
    }
}
void removeFromSolution(int pos, int capacity,set<item> & available) {
    update(pos, -1e18);
    tabu.push_back(pos);
    available.insert(items[pos]);
    if (tabu.size() > capacity) {
            int fit = tabu.front();
            if (solution[fit]) {
                available.insert(items[fit]);
            }
            tabu.pop_front();
    }
}


void assert(bool expr, string message) {
    if (expr)
        return;
}

int main (int argc, char *argv[]) {
    ios_base::sync_with_stdio(0); cin.tie(0);
    //Le la entrada
    cin >> N >> W;
    items.resize(N);
    for (int i =0;i < N; i++) {
        cin >> items[i].p >> items[i].w;
        items[i].pos=i;
    }
    sort(items.begin(), items.end());
    vector<int> bestFound(N, 0);
    data best = {0,0,0};
    data current = {0,0,0};
    int T=0;
    int repetitions = 100;
    //Probar todas las |T|
    set<item> available;
    for (auto el : items) {
        available.insert(el);
    }
    for (T=0; T < N; T++) {
        cout <<"::"<<endl;
        current={0,0,0};
        solution = vector<int> (N,0);


        for (int r =0;r < repetitions; r++) {
            //Busca al vecino
            ll capacityLeft = W-current.totalWeight;
            data next = current;
            //Try adding a positive element
            if (available.size() >0 && available.begin()->w <= capacityLeft) {
                pli candidate = findCandidate(0, upper_bound(items.begin(), items.end(),item{(ll)1e18, capacityLeft,0})-items.begin());
                //Agregamos un item
                int cid = candidate.second;
                addToSolution(cid, T, available);

                next.totalScore+=items[cid].p;
                next.totalWeight+=items[cid].w;
                next.fitness = next.totalWeight<=W?next.totalScore: -next.totalWeight;
                assert(solution[cid]==false, "Added an item that was already in solution");
                solution[cid] = true;

            } else {
                // Add lightest element
                if (available.size() > 0) {
                    int cid = available.begin()->pos;
                    addToSolution(cid, T, available);
                    next.totalScore+=items[cid].p;
                    next.totalWeight+=items[cid].w;
                    next.fitness = next.totalWeight<=W?next.totalScore: -next.totalWeight;
                    assert(solution[cid]==false, "Added an item that was already in solution");
                    solution[cid] = true;

                } else {
                    cout << "CRUSH";
                    break;
                }
            }

            current=next;

    cout <<current.fitness<<endl;
        }
    }





    return 0;
}
