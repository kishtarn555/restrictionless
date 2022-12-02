#include<iostream>
#include <functional>
#include <vector>
#include <queue>
#include <set>
#include <algorithm>
#include <utility>
#include <string>
#include <fstream>
#include <math.h>

using namespace std;

# define assert(condition,message) {if (!(condition))  {cout << "[ERROR] "<<message<<endl;exit(0);}}

using ll = long long;

struct data{
    ll weight;
    ll cost;
    pair<ll, ll> expensive,cheapest;
    pair<ll, ll> heaviest, lightest;
    int index;
    int lazy;
    int sum=0;
    data() {
    }

    data(ll w, ll c, int idx) {
        weight = w;
        cost = c;
        index=idx;
        lazy =0;
        sum=1;
        expensive = {c, idx};
        cheapest = {c, idx};
        heaviest= {w, idx};
        lightest = {w, idx};
    }
    data (ll infinite) {
        weight=infinite;
        cost = -infinite;
        sum=0;
        lazy=0;
        expensive = {-infinite, -1};
        cheapest = {infinite, -1};
        heaviest = {-infinite, -1};
        lightest = {infinite, -1};
    }

    bool operator < (const data & other) const {
        return weight < other.weight;
    }
};


vector<data> items;
int N,W;

int PID=1;
vector<int> solution;

deque<int> tabu;

// ================= SEGMENT TREE  CODE ======================================

using joinFunction = function<data(data,data)>;

data shelveJoin(data  a, data b) {
    data result = data(0);
    result.heaviest = max(a.heaviest, b.heaviest);
    result.expensive = max(a.expensive, b.expensive);
    result.lightest = min(a.lightest, b.lightest);
    result.cheapest = min(a.cheapest, b.cheapest);
    result.sum = a.sum+b.sum;
    return result;
}



data shelve[400050];
data backpack[400050];

data shelveOr[400050];
data backpackOr[400050];
///Builds both segment trees for range [l, r] and stores it at index position.
void build(int index, int l, int r) {
    // Check if it is a leave
    if (l==r) {
        //empty backpack
        backpack[index]=data(1e18);

        //shelve with l-th item
        shelve[index]=data(items[l].weight, items[l].cost, l);

        shelveOr[index]=shelve[index];
        backpackOr[index]=backpack[index];
        return;
    }
    int m =(l+r)/2;
    build(index*2, l, m); // Build left child
    build(index*2+1, m+1, r); // Build right child

    //Calculate parent values from childs
    backpack[index]= shelveJoin(backpack[index*2],backpack[index*2+1]);
    shelve[index]= shelveJoin(shelve[index*2],shelve[index*2+1]);
    //Save original for quick restore
    shelveOr[index]= shelve[index];
    backpackOr[index]= backpack[index];
}

void push(data *st, int index, int l, int r) {
    if (st[index].lazy==0)return;


    st[index].lazy=0;
    if (st == shelve) {
        st[index]= shelveOr[index];
    } else if (st == backpack){
        st[index]= backpackOr[index];
    } else {
        assert(false, "error with lazy");
    }
    if (l!=r) {
        st[2*index].lazy=1;
        st[2*index+1].lazy=1;
    }

}

void update (data * st, int index, int l, int r, int p, data value, joinFunction joiner) {
    push(st, index, l, r);
    if (l==r) {
        st[index]=value;
        return;
    }
    int m=(l+r)/2;
    if (p <= m) {
        update(st, index*2, l, m, p, value, joiner);
    } else {
        update(st, index*2+1, m+1, r, p, value, joiner);
    }
    push(st, index*2, l, m);
    push(st, index*2+1, m+1, r);
    st[index] = joiner(st[index*2], st[index*2+1]);

}


/// Queries a segment tree in range [i, j]
data query(data * st, int index, int l, int r, int i, int j, joinFunction joiner) {
    push(st, index, l, r);
    if (j < l || r < i || j<i) {
        return data(1e18);
    }
    if (i <=l && r <=j) {
        return st[index];
    }
    int m =(l+r)/2;
    return joiner(
             query(st, index*2, l,m,i,j,joiner),
             query(st, index*2+1, m+1,r,i,j,joiner)
             );
}
// ======================================================================================

void removeShelf(int pos) {
    data fix = data(1e18);
    update(shelve, 1, 0, N-1, pos, fix, shelveJoin );
}
void addShelf(int pos) {
    data fix = data(items[pos].weight, items[pos].cost, pos);
    update(shelve, 1, 0, N-1, pos, fix, shelveJoin );
}
void addBag(int pos) {
    data fix = data(items[pos].weight, items[pos].cost, pos);
    update(backpack, 1, 0, N-1, pos, fix, shelveJoin );
}
void removeBag(int pos) {
    data fix = data(1e18);
    update(backpack, 1, 0, N-1, pos, fix, shelveJoin );
}

struct values {
    ll fitness, score, weight;
};

values calculateNewValue(ll delta_weight, ll delta_cost, const values val) {
    values tmp = val;
    tmp.score += delta_cost;
    tmp.weight += delta_weight;
    tmp.fitness= tmp.score;
    if (tmp.weight > W) {
        tmp.fitness = -tmp.weight;
    }
    return tmp;
}

values addToSolution(int pos, int TabuCapacity, values val) {
    assert(solution[pos]!=PID, "Added to solution an item that was already in solution");
//    cout << "huh";
    removeShelf(pos);
    tabu.push_back(pos);
    solution[pos]=PID;

    if (tabu.size() > TabuCapacity) {

            int fit = tabu.front();
            if (solution[fit]!=PID) {
                addShelf(fit);
            } else {
                addBag(fit);
            }
            tabu.pop_front();
    }

    return calculateNewValue(items[pos].weight, items[pos].cost, val);
}
values removeFromSolution(int pos, int capacity, values val) {
    assert(solution[pos]==PID, "Removed an item that wasn't in the solution "<< solution[pos] << " "<<PID <<", capacity is: "<<capacity);
    removeBag(pos);
    tabu.push_back(pos);
    solution[pos]=0;

    if (tabu.size() > capacity) {
            int fit = tabu.front();
            if (solution[fit]!=PID) {
                addShelf(fit);
            } else {
                addBag(fit);
            }
            tabu.pop_front();
    }

    return calculateNewValue(-items[pos].weight, -items[pos].cost, val);;
}
int main (int argc, char * argv[]) {
    ios_base::sync_with_stdio(0); cin.tie(0);
    //Le la entrada
    cin >> N >> W;
    items.resize(N);
    for (int i =0;i < N; i++) {
        ll c, w;
        cin >> c >> w;
        items[i] = data(w,c,i);
        items[i].sum=1;

    }
    sort(items.begin(), items.end());

    build(1, 0, N-1);
    vector<int> bestFound(N, 0);
    solution = vector<int>(N, 0);
    values best = {0,0,0};
    values current = {0,0,0};
    int T=0;
    int tries = 1e6/N;
    if (tries < 10) tries = 10;
    int lal=0;

    for (T=3; T<4; T++) {
            PID++;
            current={0,0,0};
            shelve[1].lazy=backpack[1].lazy=1;
            tabu.clear();
        for (int jj=0; jj < tries; jj++) {

            ll capacity = W - current.weight;

            if (capacity >= 0) {
                    // La mochila no tiene sobre peso
                int p = upper_bound(items.begin(), items.end(), data(capacity,0,0))-items.begin();
                p--;

                /* Add best item that still fits*/ {
                    data mostExpensive = query(shelve, 1, 0, N-1, 0, p, shelveJoin);
                    if (mostExpensive.expensive.second >= 0) {
                        current = addToSolution(mostExpensive.expensive.second , T, current);
                        goto ENDSTEP;
                    }
                }
                /* Remove chepeast item from backpack*/ {
                    data cheapestInBackpack = query(backpack, 1, 0, N-1, 0, N-1, shelveJoin);
                    if (cheapestInBackpack.cheapest.second >= 0) {
                        current = removeFromSolution(cheapestInBackpack.cheapest.second , T, current);
                        goto ENDSTEP;
                    }
                }
                /* Add lightest item from shelve */ {
                    data lightestInShelve = query(shelve, 1, 0, N-1, 0, N-1, shelveJoin);
                    if (lightestInShelve.lightest.second >= 0) {
                        current = addToSolution(lightestInShelve.lightest.second , T, current);
                        goto ENDSTEP;
                    }
                }
            } else {
                ll overweight = -capacity;
                int p = lower_bound(items.begin(), items.end(), data(overweight,0,0))-items.begin();
                /* Try to remove cheapest item to stop being overweight */ {
                    data cheapestOverweight= query(backpack, 1, 0, N-1, p, N-1, shelveJoin);
                    if (cheapestOverweight.cheapest.second >= 0) {
                        current = removeFromSolution(cheapestOverweight.cheapest.second, T, current);
                        goto ENDSTEP;
                    }
                }

                /* Try to remove cheapest item to stop being overweight */ {
                    data heaviestInBackpack= query(backpack, 1, 0, N-1, 0, N-1, shelveJoin);
                    if (heaviestInBackpack.heaviest.second >= 0) {
                        current = removeFromSolution(heaviestInBackpack.heaviest.second, T, current);
                        goto ENDSTEP;
                    }
                }
                /* Try to add lightest */ {
                    data lightestInShelve= query(shelve, 1, 0, N-1, 0, N-1, shelveJoin);
                    if (lightestInShelve.lightest.second >= 0) {
                        current = addToSolution(lightestInShelve.lightest.second, T, current);
                        goto ENDSTEP;
                    }
                }
            }
            cout << "tabu size:" <<tabu.size()<<endl;
            cout <<"step: "<< jj<<endl;
            push(shelve, 1, 0, N-1);
            push(backpack, 1, 0, N-1);
            cout << "shelve available moves: "<<shelve[1].sum<<endl;
            cout << "backpack available moves: "<<backpack[1].sum<<endl;
            assert(false, "Found no possible move");
            ENDSTEP:
            if (current.fitness > best.fitness) {
                best.fitness=current.fitness;
                bestFound=solution;
            }
        }
    }
    ofstream output(argv[1]);
    vector<bool> rendered(N, false);
    ll weightSum=0;
    ll costSum=0;
    for (int i =0; i < N; i++) {
        if (bestFound[i]) {
            rendered[items[i].index]= true;
            weightSum+=items[i].weight;
            costSum+=items[i].cost;
        }
    }
    for (int i=0; i < N; i++) {
        output << rendered[i]<<" ";
    }
    output <<"\n";
    output << weightSum<<"\n";
    output << costSum<<"\n";

    if (weightSum > W) {
        output << "ERROR"<<"\n";
    }
    assert(weightSum <= W, "TOO HEAVY");
    assert(costSum==best.fitness, "DISCREPANCY");
    cout << best.fitness<<endl;
    output.close();

}
