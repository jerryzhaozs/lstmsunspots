#include<iostream>
#include<algorithm>
#include<cstdio>
#include<cstdlib>
#include<cmath>
#include<ctime>
#include<cstring>
#include<deque>
#include<map>
#include<queue>
#include<stack>
#include<vector>
#include<set>
#define REP(i,a,b) for(int i=(a);i<=(b);i++)
#define FOR(i,a,b) for(int i=(a);i<(b);i++)
#define int long long
using namespace std;
int n;
int m[55][55];
int tab[55][55][105][205];
int num[55][55][105];
map<int,int> ans;
int xx[4]={-1,0,1,0};
int yy[4]={0,-1,0,1};
int ten(int k){
	int res=1;
	for(int i=1;i<=k;i++){
		res*=10;
	}
	return res;
}
void have(int i,int j,int g){
	for(int k=0;k<4;k++){
		if(i+yy[k]>=1&&i+yy[k]<=n&&j+xx[k]>=1&&j+xx[k]<=n){
			// cout<<i+yy[k]<<" "<<j+xx[k]<<" "<<g<<" "<<num[i+yy[k]][j+xx[k]][g-1]<<endl;
			for(int u=1;u<=num[i+yy[k]][j+xx[k]][g-1];u++){
				tab[i][j][g][++num[i][j][g]]=ten(g-1)*m[i][j]+tab[i+yy[k]][j+xx[k]][g-1][u];
				ans[tab[i][j][g][num[i][j][g]]]=1;
				// cout<<tab[i][j][g][num[i][j][g]]<<endl;
			}
		}
	}
}
void solve(){
	cin>>n;
	for(int i=1;i<=n;i++){
		for(int j=1;j<=n;j++){
			cin>>m[i][j];
			ans[m[i][j]]=1;
			tab[i][j][1][1]=m[i][j];
			num[i][j][1]=1;
		}
	}
	for(int g=2;g<=5;g++){
		for(int i=1;i<=n;i++){
			for(int j=1;j<=n;j++){
				// cout<<"!";
				have(i,j,g);
			}
		}
	}
	int k=0;
	while(ans[k]==1){
		k++;
	}
	cout<<k<<endl;
	// cout<<num[3][3][4]<<endl;
}
signed main(){
	// int T;
	// cin>>T;
	// while(T--)
	solve();
	return 0;
}