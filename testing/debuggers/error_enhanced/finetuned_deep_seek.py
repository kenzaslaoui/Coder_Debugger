# -*- coding: utf-8 -*-
"""finetuned_deep_seek.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BGqskrbUWtPipVgEWYvgj_96QahujK8c
"""

"""
finetuned_deep_seek.py: Error-enhanced debugger using fine-tuned DeepSeek Coder
"""
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from google.colab import drive
drive.mount('/content/drive')

class FinetunedDeepSeekErrorDebugger:
    def __init__(self):
        # Path to the fine-tuned model adapter
        self.adapter_path = "/content/drive/MyDrive/Academic_Professional_Planning/SPRING2025/GEN_AI/Multi_Agent_Self_Debugger_Coder/training/finetuned/deepseek_coder_finetuned/final_finetuned_model"
        self.base_model = "deepseek-ai/deepseek-coder-6.7b-instruct"

        # Initialize model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model, trust_remote_code=True)

        # Load base model with reduced precision
        print(f"Loading base model: {self.base_model}")
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True
        )

        # Load adapter
        print(f"Loading fine-tuned adapter from: {self.adapter_path}")
        self.model = PeftModel.from_pretrained(base_model, self.adapter_path)
        self.model.eval()

        print("Fine-tuned model loaded successfully!")

    def debug_code(self, task: str, buggy_code: str, error: str, max_new_tokens: int = 512) -> str:
        """
        Error-enhanced debugging that includes error messages

        Args:
            task: Description of the task
            buggy_code: Code with bugs to be fixed
            error: Error message from executing the buggy code
            max_new_tokens: Maximum number of tokens to generate

        Returns:
            String containing the debugged code or explanation
        """
        # Format prompt for error-enhanced debugging
        full_prompt = self.format_debug_prompt(task, buggy_code, error)
        messages = [{'role': 'user', 'content': full_prompt}]

        try:
            # Prepare input
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=False,
                    top_k=50,
                    top_p=0.95,
                    temperature=0.2,
                    eos_token_id=self.tokenizer.eos_token_id
                )

            # Decode response
            fixed_code = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
            return fixed_code.strip()
        except Exception as e:
            print(f"Error in generation: {e}")
            return f"Error in generation: {e}"

    def format_debug_prompt(self, task: str, buggy_code: str, error: str) -> str:
        """
        Format the debug prompt including error information.
        """
        return (
            f"Given a programming task and its incorrect solution, your task is to fix up the incorrect solution according to the programming task and provide the correct, executable solution.\n\n"
            f"###Task:\n\n"
            f"{task}\n\n"
            f"###Incorrect Solution:\n\n"
            f"{buggy_code}\n"
            f"###Error:\n\n"
            f"{error}\n"
        )