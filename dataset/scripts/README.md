# Steps to inspect a sample locally

The `utils` script take 4 inputs: `<directory to clone into>, <sample num> <dataset_dir> <COMMAND>`

1. Run `clone` command: 
        `python utils.py ../projects/ 1 ../java/ clone`  
        This will clone the git repo into the <directory> (../projects/ in this case)  

2 Run `checkout` command:
        `python utils.py ../projects/ 1 ../java/ checkout`  
        This will put the repo in the state it was in when the comment was made  

3. Run `info` command:
        `python utils.py ../projects/ 1 ../java/ info --context {function or file}`  
        This will print the surrounding context that the comment was made on  

