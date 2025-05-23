# -*- coding: utf-8 -*-
"""base_deep_seek.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oDZiJ5J5MJLjVw3I8bFruo9W54yeSNAi
"""

"""
base_deep_seek.py: Zero-shot debugger using base DeepSeek Coder
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class BaseDeepSeekDebugger:
    def __init__(self):
        # Base model without fine-tuning
        self.model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"

        # Initialize model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)

        print(f"Loading model: {self.model_name}")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True
        )
        self.model.eval()

        print("Base model loaded successfully!")

    def debug_code(self, task: str, buggy_code: str, max_new_tokens: int = 512) -> str:
        """Zero-shot debugging (no error message)"""
        # Format prompt for zero-shot debugging
        full_prompt = self.format_debug_prompt(task, buggy_code)
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

    def format_debug_prompt(self, task: str, buggy_code: str) -> str:
        """Format prompt for zero-shot debugging"""
        return (
            f"You are a helpful AI coding assistant.\n"
            f"The user was trying to solve the following task:\n"
            f"{task}\n\n"
            f"The code they wrote is:\n{buggy_code}\n\n"
            f"Please provide the corrected version of the code.\n"
        )