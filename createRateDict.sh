#for run in 322079 322088 323940 324293 324970 325022
#for run in 322088 323940 324293 324970 325022
#do
#    python rate.py --runnum ${run} &
#done


#xvar="npu"

#for pt in $(seq 3 10)
for pt in $(seq 3 10)
do
    sel="mu1_pt>=${pt}"
    name="singleMu${pt}"
    echo $sel, $name
    python ratedep.py --name ${name} --sel ${sel}

done


for pt in $(seq 3 10)
do

    name="mu4_eg${pt}"
    sel="mu1_pt>=4&&e1_pt>=${pt}"
    echo $sel, $name
    python ratedep.py --name ${name} --sel ${sel}

done


for pt in $(seq 3 10)
do

    name="mu4_DoubleE_eta1p5_${pt}"
    sel="mu1_pt>=4&&doubleE_eta1p5_${pt}==1"
    echo $sel, $name
    python ratedep.py --name ${name} --sel ${sel}

done


for pt in $(seq 3 10)
do
    name="DoubleE${pt}"
    sel="doubleE${pt}==1"
    echo $sel, $name

    python ratedep.py --name ${name} --sel ${sel}

done



for pt in $(seq 3 6)
do
    name="E7_E${pt}"
    sel="E7_E${pt}==1"
    echo $sel, $name

    python ratedep.py --name ${name} --sel ${sel}

done



for pt in $(seq 3 7)
do
    name="E8_E${pt}"
    sel="E8_E${pt}==1"
    echo $sel, $name

    python ratedep.py --name ${name} --sel ${sel}

done

for pt in $(seq 3 8)
do
    name="E9_E${pt}"
    sel="E9_E${pt}==1"
    echo $sel, $name

    python ratedep.py --name ${name} --sel ${sel}

done


for pt in $(seq 3 9)
do
    name="E10_E${pt}"
    sel="E10_E${pt}==1"
    echo $sel, $name

    python ratedep.py --name ${name} --sel ${sel}

done


