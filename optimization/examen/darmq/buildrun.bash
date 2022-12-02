#!/bin/bash

g++ rmq2.cpp -o rmq

echo "---"
echo "ks_4_0"
./rmq < cases/ks_4_0
echo "---"
echo "ks_19_0"
./rmq < cases/ks_19_0
echo "---"
echo "ks_30_0"      
./rmq < cases/ks_30_0
echo "---"
echo "ks_40_0"      
./rmq < cases/ks_40_0
echo "---"
echo "ks_45_0"      
./rmq < cases/ks_45_0
echo "---"
echo "ks_50_0"      
./rmq < cases/ks_50_0
echo "---"
echo "ks_50_1"      
./rmq < cases/ks_50_1
echo "---"
echo "ks_60_0"      
./rmq < cases/ks_60_0
echo "---"
echo "ks_82_0"      
./rmq < cases/ks_82_0
echo "---"
echo "ks_100_0"      
./rmq < cases/ks_100_0
echo "---"
echo "ks_100_1"      
./rmq < cases/ks_100_1
echo "---"
echo "ks_100_2"      
./rmq < cases/ks_100_2
echo "---"
echo "ks_106_0"      
./rmq < cases/ks_106_0
echo "---"
echo "ks_200_0"      
./rmq < cases/ks_200_0
echo "---"
echo "ks_200_1"      
./rmq < cases/ks_200_1
echo "---"
echo "ks_300_0"      
./rmq < cases/ks_300_0
echo "---"
echo "ks_400_0"      
./rmq < cases/ks_400_0
echo "---"
echo "ks_500_0"      
./rmq < cases/ks_500_0
echo "---"
echo "ks_1000_0"     
./rmq < cases/ks_1000_0
echo "---"
echo "ks_10000_0"
./rmq < cases/ks_10000_0