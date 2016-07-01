#include <fstream>
#include <string>
#include <sstream>
#include <map>
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <cstring>
#include <ctime>

using namespace std;


//map<string, string> filter;
map<string, pair<float, float> > macLonlat;
map<string, int> macCtgy;
map<string, vector<float> > macDistance;
//map<string, set<int> > userTime;

typedef pair<string, pair<float, float> > PAIR;


bool cmp_by_value(const PAIR& lhs, const PAIR& rhs){
    return lhs.second.size() > rhs.second.size();
}


//目标函数
void getDistanceMatrix(){

    vector<PAIR > cPair(macLonlat.begin(),macLonlat.end());
    //sort(cPair.begin(), cPair.end(), cmp_by_value);
    string mac;
    for(int i = 0; i<cPair.size(); ++i){
        mac = cPair[i].first;
        for(int j = 0; j<cPair.size(); ++j){
            dist = (cPair[i].second, cPair[j].second);
            macDistance[mac].push_back(dist);
        }





        if(cPair[i].second.size() >= 2){
          //for(set<string>::const_iterator it=cPair[i].second.begin();it!=cPair[i].second.end(); ++it){
            vector<string> v(cPair[i].second.begin(),cPair[i].second.end());
            for(int j=0; j<v.size()-1;j++){
              for(int h=j+1;h<v.size();h++){
                  ofs2<<v[j]<<','<<v[h]<<endl;
              }
            }
          }
        else{
          for(set<string>::const_iterator it=cPair[i].second.begin();it!=cPair[i].second.end(); ++it){
            ofs1<<*it<<endl;
          }
        }
      }


}

int main(int argc, char* argv[]){

   string s1 = argv[1];//"buptpoi16_22_intCatagory_block_trainset"
   string s2 = argv[2];//"buptpoi16_22_intCatagory_block_testset"

   ifstream ifs1(s1.c_str());
   string mac, token, line;
   float lon=0.0, lat=0.0;
   int catagory = 0;
   int count = 0;
   while(getline(ifs1, line)){
       istringstream iss(line);
       count=0;
       while(getline(iss, token, ' ')){
           count ++;
           switch(count){
           case 2:
               mac = token;
               break;
           case 3:
               lon = float(token);
               break;
           case 4:
               lat = float(token);
               break;
           case 8:
               catagory = int(token);
               break;
           }
       }
       macLonlat[mac].insert(make_pair(lon,lat));
       macCtgy[mac].insert(catagory);
   }
   ifs1.close();

   ifstream ifs2(s2.c_str());
   //string mac, token, line;
   //float lon=0.0, lat=0.0;
   //int catagory = 0;
   //int count = 0;
   while(getline(ifs2, line)){
       istringstream iss(line);
       count=0;
       while(getline(iss, token, ' ')){
           count ++;
           switch(count){
           case 2:
               mac = token;
               break;
           case 3:
               lon = float(token);
               break;
           case 4:
               lat = float(token);
               break;
           //case 8:
            //   catagory = int(token);
            //   break;
           }
       }
       macLonlat[mac].insert(make_pair(lon,lat));
       macCtgy[mac].insert(0);  //测试集的catagory设为0，表示未知
   }
   ifs2.close();

   getDistanceMatrix();





}
