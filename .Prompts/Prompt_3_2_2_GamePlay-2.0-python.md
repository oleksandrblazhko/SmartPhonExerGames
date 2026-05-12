

cat .Prompts/Prompt_3_2_1_GamePlay-2.0.md | gemini --yolo

for i in {1..20}
do
   cat prompt.md | gemini --yolo > results/run_$i.md
   sleep 2
done
