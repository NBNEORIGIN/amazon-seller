import os
import json
from typing import List, Dict, Any
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaConfig

class LlamaInterface:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = "C:/Users/zentu/.llama/checkpoints/Llama3.2-1B"
        self.load_model()

    def load_model(self):
        try:
            # Create config
            config = LlamaConfig(
                vocab_size=32000,  # Standard for Llama
                hidden_size=4096,
                intermediate_size=11008,
                num_hidden_layers=32,
                num_attention_heads=32,
                max_position_embeddings=4096,
                rms_norm_eps=1e-6,
                pad_token_id=0,
                bos_token_id=1,
                eos_token_id=2,
            )
            
            # Load state dict
            state_dict = torch.load(
                os.path.join(self.model_path, "consolidated.00.pth"),
                map_location=self.device
            )
            
            # Create model
            self.model = AutoModelForCausalLM.from_config(config)
            self.model.load_state_dict(state_dict, strict=False)
            self.model.to(self.device)
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            print("Llama 3.2-1B model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
        
    def analyze_design(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a design file and provide QA feedback"""
        prompt = f"""Please analyze this memorial design data and provide QA feedback:
        {json.dumps(design_data, indent=2)}
        
        Please check for:
        1. Spelling and grammar
        2. Design consistency
        3. Measurements and proportions
        4. Any potential production issues
        
        Provide feedback in JSON format with these keys:
        - issues_found: list of problems
        - suggestions: list of improvements
        - is_approved: boolean
        """
        
        try:
            if not self.model:
                if not self.load_model():
                    return {
                        "issues_found": ["Model not loaded"],
                        "suggestions": [],
                        "is_approved": False
                    }
            
            system_prompt = "You are a helpful AI assistant specializing in memorial product design quality assurance. You analyze designs and provide detailed feedback in JSON format."
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Generate response
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=2048,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.15,
                do_sample=True
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract JSON from response
            json_str = response[response.find('{'):response.rfind('}')+1]
            return json.loads(json_str)
        except Exception as e:
            print(f"Error in design analysis: {str(e)}")
            return {
                "issues_found": ["Error processing design with LLM"],
                "suggestions": [],
                "is_approved": False
            }
    
    def analyze_inventory(self, inventory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze inventory data and provide insights"""
        prompt = f"""Please analyze this FBA inventory data and provide insights:
        {json.dumps(inventory_data, indent=2)}
        
        Please provide:
        1. Stock level analysis
        2. Reorder recommendations
        3. Sales velocity insights
        4. Storage fee optimization suggestions
        
        Provide feedback in JSON format with these keys:
        - insights: list of key findings
        - recommendations: list of actions
        - priority_items: list of SKUs needing immediate attention
        """
        
        try:
            if not self.model:
                if not self.load_model():
                    return {
                        "insights": ["Model not loaded"],
                        "recommendations": [],
                        "priority_items": []
                    }
            
            system_prompt = "You are a helpful AI assistant specializing in inventory analysis and optimization. You analyze inventory data and provide actionable insights in JSON format."
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Generate response
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=2048,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.15,
                do_sample=True
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract JSON from response
            json_str = response[response.find('{'):response.rfind('}')+1]
            return json.loads(json_str)
        except Exception as e:
            print(f"Error in inventory analysis: {str(e)}")
            return {
                "insights": ["Error processing inventory with LLM"],
                "recommendations": [],
                "priority_items": []
            }

    def qa_check_orders(self, orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """QA check for order data before processing"""
        prompt = f"""Please analyze these memorial orders for potential issues:
        {json.dumps(orders, indent=2)}
        
        Check for:
        1. Missing required fields
        2. Inconsistent measurements
        3. Invalid color combinations
        4. Text formatting issues
        5. Production feasibility
        
        For each order, provide feedback in JSON format with these keys:
        - order_id: string
        - issues: list of problems
        - suggestions: list of fixes
        - can_proceed: boolean
        """
        
        try:
            if not self.model:
                if not self.load_model():
                    return [{
                        "order_id": order.get("order-id", "unknown"),
                        "issues": ["Model not loaded"],
                        "suggestions": [],
                        "can_proceed": False
                    } for order in orders]
            
            system_prompt = "You are a helpful AI assistant specializing in memorial product order validation. You analyze orders and provide detailed feedback in JSON format."
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Generate response
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=2048,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.15,
                do_sample=True
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract JSON from response
            json_str = response[response.find('['):response.rfind(']')+1]
            return json.loads(json_str)
        except Exception as e:
            print(f"Error in order QA: {str(e)}")
            return [{
                "order_id": order.get("order-id", "unknown"),
                "issues": ["Error processing order with LLM"],
                "suggestions": [],
                "can_proceed": False
            } for order in orders]

# Example usage
if __name__ == "__main__":
    llm = LlamaInterface()
    
    # Test design analysis
    test_design = {
        "type": "memorial_stake",
        "dimensions": {"width": 140, "height": 90},
        "text": ["In Loving Memory", "John Smith", "1945 - 2024"]
    }
    result = llm.analyze_design(test_design)
    print("Design Analysis:", json.dumps(result, indent=2))
