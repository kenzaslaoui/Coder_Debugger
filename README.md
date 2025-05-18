This is a generative AI project that uses LLMs to generate and debug code. 

There are two main components to this project:

1. We finetune a code generation LLM "Deepseek Coder 6.7B intruct" on code debugging data to teach the model to identify and fix bugs. We use quantized LoRA and implement the finetuning process on Google Colab due to resource constraints. The model is finetuned on Python, Java and C++ code.

2. We create a user-oriented pipeline, that takes as input (a programing task, test cases for the task, and the programming language) from a user, and outputs code.
This pipeline relies on a "generator" that uses the base DeepSeek Coder 6.7B intruct to generate the code for the task. The generated code is then passed to an "executor" that takes in the generated code and test cases and returns the errors in the code if any. These errors, along with the buggy code, the initial task and the test cases are then passed to the "debugger", which uses our finetuned model to fix the code - which is then returned to the user.
This process is facilitated by a "coordinator" which uses LangChain and GPT-4o-mini to orchestrate this process.
This pipeline allows users to ask for code in any of Python, Java or C++

We test our results and compare our finetuned model with the base model on the pass@ rate, the success rate based on language, and the success rate based on the bug type in the code. While our results show a modest performance, considering that this work was done on limited resources, they remain a promising stepping stone for a much better debugger model in the future.

Note: Most of the files in this project were generated from jupyter notebooks as I needed to use google colab for both training and inference.

I could not push the finetuned model to github due to resource constraints. However, you can access it through this link: 
https://drive.google.com/drive/folders/1Uh1uj1Ih4L3GWQ2Bk1pVDm0e_wDxjNU1?usp=sharing

The following is a tutorial to help guide you through this repo:

- training 
  -  data folder: contains data.json - this is the data used for training
  -  finetuning folder: containing finetune_qlora.ipynb - this notebook shows the entire finetuning process and results
  
- testing
  - test_data: contains parsed_debugbench_samples.json - this is the test set we parsed and formatted using the orginal test set provided by DebugBench
  - debuggers: contains 4 zero shot debuggers and 4 error enhanced debuggers of the following models(code llama 7b, starcoder2 7b, base deepseek coder 6.7b, and finetuned deepseek coder 6.7b)
  - results:
      - 2 plots of the results comparing the base and finetuned model based on bug type and programming language 
        (language_success_20250518_152054.png, bug_type_success_20250518_152055.png)
      - debugbench_results_20250518_152054.json: shows all final results and intermediate results of the testing
        
- agents
  - generator.py: based on the base deepseek model - this is the generator for the user-pipeline
  - executor.py: executes code with test cases for Python, Java, and C++ and supports the user-pipeline and the testing process
  - debugger.py: based on the finetuned model - this is the debugger used for the user-pipeline
  
- coordinator
  - pipeline_coordinator.py: this is the coordinator for the user-pipeline which uses GPT 4o mini and LangChain for orchestration between agents   


