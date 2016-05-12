# put any stuff to install here

python setup.py

IFS=$'\n' read -d '' -r -a lines < app_names.txt

for i in "${lines[@]}"
do
	python Phase1/start.py $i
	python Phase2/stage2.py $i
	bash Phase3/run_phase3.sh $i
done