#include<iostream>
#include <functional>
#include <vector>
#include <queue>
#include <set>
#include <algorithm>
#include <utility>


using namespace std;
using ll = long long;

struct data{
    ll weight;
    ll cost;
    pair<ll, ll> expensive,cheapest;
    pair<ll, ll> heaviest, lightest;
    ll value;
    int index;
    int lazy;
    int sum=0;
    data() {
    }

    data(ll w, ll c, ll val, int idx) {
        weight = w;
        cost = c;
        value = val;
        index=idx;
        lazy =0;
        sum=0;
        expensive = {c, idx};
        cheapest = {c, idx};
        heaviest= {w, idx};
        lightest = {w, idx};
    }
    data (ll infinite) {
        weight=infinite;
        cost = -infinite;
        index=-1;
        lazy=sum=0;
        expensive = {-infinite, -1};
        cheapest = {infinite, -1};
        heaviest= {-infinite, -1};
        lightest = {infinite, -1};
    }
    bool operator < (const data & other) const {
        return weight < other.weight;
    }
};
using joinFunction = function<data(data,data)>;

data shelveJoin(data  a, data b) {
    data result;
    result.heaviest = max(a.heaviest, b.heaviest);
    result.expensive = max(a.expensive, b.expensive);
    result.expensive = max(a.expensive, b.expensive);
    result.sum = a.sum+b.sum;
    return result;
}
data minorJoiner(data  a, data b) {
    data result;
    if (a.value < 0)
        result = b;
    else if (b.value < 0) {
        result=a;
    } else if (a.value < b.value) {
        result=a;
    } else {
        result= b;
    }
    result.sum = a.sum+b.sum;
    return result;
}


data shelve[400050];
data backpack[400050];
data backpack2[400050];

data shelveOr[400050];
data backpackOr[400050];
data backpack2Or[400050];

vector<data> items;
int N,W;

vector<int> solution;

deque<int> tabu;

void push(data *st, int index, int l, int r) {
    if (st[index].lazy==0)return;

    st[index].lazy=0;
    if (st == shelve) {
        st[index]= shelveOr[index];
    } else if (st == backpackOr){
        st[index]= backpackOr[index];
    } else {
        st[index]= backpack2Or[index];
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
    st[index] = joiner(st[index*2], st[index*2+1]);

}

void build(int index, int l, int r) {
    if (l==r) {
        backpack[index]=items[l];
        shelve[index]=items[l];
        backpack[index].value=-1e18;
        shelve[index].value=items[l].cost;
        backpack[index].index=l;
        shelve[index].index=l;

        backpack[index].sum=0;
        backpack2[index]=backpack[index];
        shelveOr[index]=shelve[index];
        backpackOr[index]=backpack[index];
        backpack2Or[index]=backpack[index];
        return;
    }
    int m =(l+r)/2;
    build(index*2, l, m);
    build(index*2+1, m+1, r);
    backpack[index]= shelveJoin(backpack[index*2],backpack[index*2+1]);
    shelve[index]= shelveJoin(shelve[index*2],shelve[index*2+1]);
    backpack2[index]= minorJoiner(backpack2[index*2],backpack2[index*2+1]);
    //SAVE ORIGINAL FOR FAST RESTORE
    shelveOr[index]= shelve[index];
    backpackOr[index]= backpack[index];
    backpack2Or[index]= backpack2[index];
}

data query(data * st, int index, int l, int r, int i, int j, joinFunction f) {
        push(st, index, l, r);

    if (j < l || r < i || j<i) {
        return data(-1e18, -1e8, -1e18, -1);
    }
    if (i <=l && r <=j) {
        return st[index];
    }
    int m =(l+r)/2;
    return f(
             query(st, index*2, l,m,i,j,f),
             query(st, index*2+1, m+1,r,i,j,f)
             );
}


void removeShelf(int pos) {
    data fix = items[pos];
    fix.value = -1e18;
    fix.sum=0;
    fix.index=pos;
    update(shelve, 1, 0, N-1, pos, fix, shelveJoin );
}
void addShelf(int pos) {
    data fix = items[pos];
    fix.value = items[pos].cost;
    fix.sum=1;
    fix.index=pos;
    update(shelve, 1, 0, N-1, pos, fix, shelveJoin );
}
void removeBag(int pos) {
    data fix = items[pos];
    fix.value = -1e18;
    fix.sum=0;
    fix.index=pos;
    data f2 = fix;
    update(backpack, 1, 0, N-1, pos, fix, shelveJoin );
    update(backpack2, 1, 0, N-1, pos, fix, minorJoiner );
}
void addBag(int pos) {
    data fix = items[pos];
    fix.value = items[pos].weight;
    fix.sum=1;
    fix.index=pos;
    update(backpack, 1, 0, N-1, pos, fix, shelveJoin );
}
struct values {
    ll fitness, score, weight;
};

int PID=1;

values addToSolution(int pos, int capacity, values val) {
    removeShelf(pos);
    tabu.push_back(pos);
    solution[pos]=PID;

    if (tabu.size() > capacity) {
            int fit = tabu.front();
            if (solution[fit]!=PID) {
                addShelf(fit);
            } else {
                addBag(fit);
            }
            tabu.pop_front();
    }

    val.score += items[pos].cost;
    val.weight += items[pos].weight;
    val.fitness= val.score;
    if (val.weight > W) {
        val.fitness = -val.weight;
    }
    return val;
}
values removeSolution(int pos, int capacity, values val) {
    if (solution[pos]!= PID) {
        cout << "ERRR";
        return values();
    }
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

    val.score -= items[pos].cost;
    val.weight -= items[pos].weight;
    val.fitness= val.score;
    if (val.weight > W) {
        val.fitness = -val.weight;
    }
    return val;
}
int main () {
    ios_base::sync_with_stdio(0); cin.tie(0);
    //Le la entrada
    cin >> N >> W;
    items.resize(N);
    for (int i =0;i < N; i++) {
        ll c, w;
        cin >> c >> w;
        items[i] = data(w,c,c,i);
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
    for (T=0; T<N; T++) {
            PID++;
            current={0,0,0};
            if (T!=0)
            shelve[1].lazy=backpack[1].lazy=1;
            tabu.clear();
        for (int jj=0; jj < tries; jj++) {

            ll capacity = W - current.weight;
            int p = upper_bound(items.begin(), items.end(), data(capacity,0,0,0))-items.begin();
            p--;
            data result = query(shelve,1, 0, N-1,0,p, shelveJoin);
            if (result.value > 0) {
                    lal++;
                current = addToSolution(result.index, T, current);
            }
            if (current.fitness > best.fitness) {
                best=current;
                bestFound=solution;
            } else {
                data result = query(backpack,1, 0, N-1,0,N-1, shelveJoin);
                if (result.value > 0)  {
                    if (solution[ result.index]!=PID) {
                        cout << lal<<endl;
                        cout << T<<" "<<result.sum<<" "<<result.weight << " "<<result.index<<"?"<<endl;
                        cout << "sol:"<<solution[result.index]<<"?"<<endl;
                        for (int  i=0;i  < N; i++) {
                            if (solution[i]==PID) {
                                cout << "\t"<<items[i].index;
                            }
                        }
                        cout << "\n";

                        for (int  i=0;i  < N; i++) {
                            if (solution[i]==PID) {
                                cout << "\t"<<items[i].weight;
                            }
                        }
                        cout << "\n";
                        cout << "backpack:" << backpack[1].value << " "<<endl;
                        return 0;
                    }
                    current = removeSolution(result.index, T, current);
                }
            }
        }
    }
    cout << best.fitness<<endl;

}
