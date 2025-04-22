from typing import Dict, Any, List, Optional
from chatbot.greetings import get_greeting
from chatbot.intent_manager import IntentManager
from chatbot.llm import GroqPCOSAdvisor

class PCOSChatEngine:
    def __init__(self):
        self.intent_manager = IntentManager("data/intents.json")
        self.llm_advisor = GroqPCOSAdvisor()
        self.active_flows: Dict[str, Any] = {}
        self.greeting_triggers = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]

        # Enhanced flows with better triggers and follow-ups
        self.flows = {
            "nutrition": {
                "triggers": ["nutrition", "diet", "meal", "food", "eat", "recipes", "healthy eating"],
                "start_question": "Let's plan your PCOS-friendly meals! What's your primary goal?",
                "options": [
                    ("Weight management", "weight"),
                    ("Hormone balance", "hormone"),
                    ("Energy boost", "energy"),
                    ("Recipe ideas", "recipes")
                ],
                "follow_up": {
                    "weight": {
                        "question": "Great! Which approach interests you most?",
                        "options": [
                            ("🍳 High-protein meals", "protein"),
                            ("🥑 Healthy fats focus", "fats"),
                            ("🌱 Plant-based options", "plant")
                        ]
                    },
                    "hormone": {
                        "question": "Which nutrient are you more focused on for hormonal balance?",
                        "options": [
                            ("Omega-3 rich meals", "omega"),
                            ("Zinc & Magnesium focused diet", "zinc_mag"),
                            ("Antioxidant-rich foods", "antioxidant")
                        ]
                    },
                    "energy": {
                        "question": "What type of meals do you prefer for energy?",
                        "options": [
                            ("Slow-digesting carbs", "slow_carb"),
                            ("Iron-rich foods", "iron"),
                            ("Light frequent meals", "frequent")
                        ]
                    },
                    "recipes": {
                        "question": "What type of recipes are you looking for?",
                        "options": [
                            ("Quick & easy", "quick"),
                            ("Meal prep friendly", "meal_prep"),
                            ("Special occasions", "special")
                        ]
                    }
                }
            },
            "pcos_check": {
                "triggers": ["check","check for pcos", "do i have pcos", "pcos test", "pcos symptoms"],
                "start_question": "Let's check for PCOS. Do you have:",
                "options": [
                    ("Ultrasound report to upload", "ultrasound_check"),
                    ("Just learning about PCOS", "learn_more")
                ],
                "follow_up": {
                    "ultrasound_check": {
                        "question": "Is your ultrasound report recent (within 6 months)?",
                        "options": [
                            ("Yes", "recent"),
                            ("No", "old")
                        ]
                    },
                    "self_diagnosis": {
                        "question": "Do you experience irregular periods or excess hair growth?",
                        "options": [
                            ("Yes", "irregular"),
                            ("No", "regular")
                        ]
                    },
                    "learn_more": {
                        "question": "Would you like general information or symptom checker?",
                        "options": [
                            ("General PCOS info", "general_info"),
                            ("Symptom checker", "symptom_checker")
                        ]
                    }
                }
            },
            "fitness": {
                "triggers": ["exercise", "workout", "fitness", "yoga", "gym"],
                "start_question": "Need a workout plan for PCOS? Choose your style:",
                "options": [
                    ("🧘 Yoga & flexibility", "yoga"),
                    ("🏋️ Strength training", "strength"),
                    ("🚶‍♀️ Low-impact cardio", "cardio"),
                    ("🤸‍♀️ Custom plan", "custom")
                ],
                "follow_up": {
                    "yoga": {
                        "question": "What's your yoga experience level?",
                        "options": [
                            ("Beginner", "beginner"),
                            ("Intermediate", "intermediate"),
                            ("Advanced", "advanced")
                        ]
                    },
                    "strength": {
                        "question": "Do you have access to gym equipment?",
                        "options": [
                            ("Yes", "gym"),
                            ("No, home workouts", "home"),
                            ("Some basic equipment", "basic")
                        ]
                    },
                    "cardio": {
                        "question": "What's your preferred cardio intensity?",
                        "options": [
                            ("Low (walking, swimming)", "low"),
                            ("Medium (cycling, dance)", "medium"),
                            ("High (HIIT, running)", "high")
                        ]
                    }
                }
            },
            "gynecologist": {
                "triggers": ["doctor", "gynecologist", "gyno", "specialist"],
                "start_question": "I can help you find a specialist nearby. Would you like to:",
                "options": [
                    ("📍 Search gynecologists near me", "find_nearby"),
                    ("💻 Book online consultation", "online")
                ]
            },
            "pharmacy": {
                "triggers": ["pharmacy", "medicine", "medication", "supplements"],
                "start_question": "Need help with medications or supplements?",
                "options": [
                    ("🏪 Find nearby pharmacy", "find_pharmacy")
                ]
            }
        }

    def _is_greeting(self, message: str) -> bool:
        return any(greet in message.lower() for greet in self.greeting_triggers)

    def handle_message(self, user_id: str, message: str) -> Dict[str, Any]:
        try:
            cleaned_msg = message.lower().strip()

            if self._is_greeting(cleaned_msg):
                return {
                    "response": get_greeting(),
                    "options": [
                        {"text": "Nutrition", "value": "nutrition"},
                        {"text": "Fitness", "value": "fitness"},
                        {"text": "PCOS Check", "value": "pcos_check"},
                        {"text": "Find Specialist", "value": "gynecologist"}
                    ],
                    "redirect": None
                }

            if user_id in self.active_flows:
                return self._continue_flow(user_id, cleaned_msg)

            # Enhanced intent detection with flow triggers
            for flow_name, flow_data in self.flows.items():
                if any(trigger in cleaned_msg for trigger in flow_data["triggers"]):
                    return self._start_flow(user_id, flow_name)

            # Fallback to LLM with options
            llm_response = self.llm_advisor.get_response(cleaned_msg)
            return {
                "response": llm_response,
                "options": [
                    {"text": "Nutrition Help", "value": "nutrition"},
                    {"text": "Fitness Advice", "value": "fitness"},
                    {"text" : "Nearby gynecologist", "value": "gynecologist"},  
                    {"text": "Medication info", "value": "pharmacy"}
                ],
                "redirect": None
            }

        except Exception as e:
            return {
                "response": f"⚠️ Sorry, I encountered an error: {str(e)}",
                "options": None,
                "redirect": None
            }

    def _start_flow(self, user_id: str, flow_name: str) -> Dict[str, Any]:
        flow = self.flows.get(flow_name)
        if not flow:
            return {
                "response": "Sorry, I couldn't start that conversation.",
                "options": None,
                "redirect": None
            }

        self.active_flows[user_id] = {
            "flow_name": flow_name,
            "step": 0,
            "data": {}
        }

        return {
            "response": flow["start_question"],
            "options": [{"text": t, "value": v} for t, v in flow["options"]],
            "redirect": None
        }

    def _continue_flow(self, user_id: str, message: str) -> Dict[str, Any]:
        try:
            flow = self.active_flows[user_id]
            flow_name = flow["flow_name"]
            current_flow = self.flows[flow_name]

            # Handle all flow-specific options
            if flow_name == "pcos_check":
                if message == "ultrasound_check":
                    del self.active_flows[user_id]
                    return {
                        "response": "You can upload ultrasound images in our 👉 <a href='/ultrasound' style='color:#ff6b88;font-weight:bold'>PCOS Ultrasound Detector</a>",
                        "options": None,
                        "redirect": "/ultrasound"
                    }
                elif message == "self_diagnosis":
                    del self.active_flows[user_id]
                    return {
                        "response": "Please proceed to our 👉 <a href='/self-diagnosis' style='color:#ff6b88;font-weight:bold'>PCOS Symptom Checker</a>",
                        "options": None,
                        "redirect": "/self-diagnosis"
                    }

            elif flow_name == "gynecologist":
                if message == "find_nearby":
                    del self.active_flows[user_id]
                    return {
                        "response": "🔍 Please allow location access and visit our <a href='/gynecologist' style='color:#ff6b88;font-weight:bold'>Gynecologist Finder</a>",
                        "options": None,
                        "redirect": "/gynecologist"
                    }
                elif message == "online":
                    del self.active_flows[user_id]
                    return {
                        "response": "💻 You can book online consultations at 👉 <a href='/telemedicine' style='color:#ff6b88;font-weight:bold'>PCOS Telemedicine</a>",
                        "options": None,
                        "redirect": "/gynecologist"
                    }

            elif flow_name == "pharmacy":
                if message == "find_pharmacy":
                    del self.active_flows[user_id]
                    return {
                        "response": "🏪 Find pharmacies near you at 👉 <a href='/pharmacy-locator' style='color:#ff6b88;font-weight:bold'>Pharmacy Locator</a>",
                        "options": None,
                        "redirect": "/pharmacy"
                    }

            # Save user's answer
            flow["data"][f"step_{flow['step']}"] = message
            flow["step"] += 1

            # Handle follow-up questions
            if "follow_up" in current_flow:
                last_answer = list(flow["data"].values())[-1]
                follow_up = current_flow["follow_up"].get(last_answer)
                if follow_up:
                    return {
                        "response": follow_up["question"],
                        "options": [{"text": t, "value": v} for t, v in follow_up["options"]],
                        "redirect": None
                    }

            # End flow with final response
            del self.active_flows[user_id]
            return self._generate_final_response(flow_name, flow["data"])

        except Exception as e:
            del self.active_flows[user_id]
            return {
                "response": f"⚠️ Flow error: {str(e)}",
                "options": None,
                "redirect": None
            }

    def _generate_final_response(self, flow_name: str, data: Dict) -> Dict[str, Any]:
        responses = {
            "nutrition": {
                "response": (
                    f"✅ Thanks for sharing! Based on your preferences:\n"
                    f"• Focus on {data.get('step_1', 'balanced')} meals\n"
                    f"• Consider {data.get('step_2', 'varied')} options\n\n"
                    f"See personalized plans at 👉 <a href='/nutrition' style='color:#ff6b88;font-weight:bold'>Nutrition Center</a>"
                ),
            },
            "fitness": {
                "response": (
                    f"🏃‍♀️ Your {data.get('step_0', 'fitness')} plan is ready!\n"
                    f"Focus on {data.get('step_1', 'consistent')} workouts\n\n"
                    f"Check routines at 👉 <a href='/fitness' style='color:#ff6b88;font-weight:bold'>Fitness Hub</a>"
                ),
            },
            "gynecologist": {
                "response": (
                    f"📍 Specialist information ready!\n\n"
                    f"Visit 👉 <a href='/gynecologist' style='color:#ff6b88;font-weight:bold'>Gynecologist Resources</a>"
                ),
                "options": [
                    {"text": "Appointment Tips", "value": "tips"},
                    {"text": "Questions to Ask", "value": "questions"}
                ]
            },
            "pharmacy": {
                "response": (
                    f"🧾 Your medication/supplement information:\n\n"
                    f"Visit 👉 <a href='/pharmacy' style='color:#ff6b88;font-weight:bold'>Pharmacy Hub</a>"
                ),
                "options": [
                    {"text": "Medication Guide", "value": "meds"},
                    {"text": "Supplement List", "value": "supplements"}
                ]
            },
            "pcos_check": {
                "response": (
                    f"✔️ PCOS checkup information ready!\n\n"
                    f"Continue at 👉 <a href='/pcos-check' style='color:#ff6b88;font-weight:bold'>PCOS Assessment</a>"
                ),
                "options": [
                    {"text": "Symptom Tracker", "value": "tracker"},
                    {"text": "Treatment Options", "value": "treatments"}
                ]
            }
        }

        return responses.get(flow_name, {
            "response": "✅ Thank you! We've noted your responses.",
            "options": [
                {"text": "Main Menu", "value": "menu"},
                {"text": "More Help", "value": "help"}
            ],
            "redirect": None
        })