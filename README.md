# Trigger studies for a BParking data set during Run 3

This code is used to estimate the performance of various trigger configurations aimed at an RK analysis in Run 3.


Copy files:
```
mkdir root;
cp /afs/cern.ch/user/y/ytakahas/public/forRob/*.root root/
```


## Produce ntuples for trigger efficiency and rate estimation

Produce ntuples:
```
. setup_rob.sh # init
python genstudy_l1.py
python rate.py
```

Trigger efficiency vs rate:
```
python generateGraphs.py --type ult
python generateGraphs.py --type rate --lumi 0.8 [you can also choose whatever value you want]
python draw_roc.py --lumi 0.8 [you can also choose whatever value you want]
evince plots/roc_ult.pdf
```

Analysis efficiency map:
```
cd eff/
root -l numer.C+
root -l denom.C+
python eff.py
cd ../
```

Trigger efficiency x signal acceptance x analysis efficiency:
```
python generateGraphs.py --type ult --weight
python generateGraphs.py --type rate
python draw_roc.py
evince plots/roc_ult.pdf
```


