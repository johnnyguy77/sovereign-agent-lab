"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                 
How many guests are you confirming for tonight's event?
Your input ->  160                                                                          
And how many of those guests will need vegan meals?
Your input ->  about 50                                                                     
2026-04-13 23:54:56 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user said "about 50" in response to the AI asking how many guests need vegan meals. The current flow is confirm_booking, and the active step is requesting the vegan_count slot.

First, I need to set the vegan_count slot to 50. The user mentioned "about 50," but the slot expects a numerical value. Since the user provided "50" as the number, even with "about," the exact value to set is 50. The slot type is float, so it should be "50.0" maybe? Wait, the guest_count was set to "160.0" when the user said "160". So probably, even if the user says "about 50", the value should be stored as a float. So I should set slot vegan_count to 50.0.

Then, after setting that slot, the next step in the flow would be to ask for the deposit amount. But according to the available flows, the confirm_booking flow has three slots: guest_count, vegan_count, and deposit_amount_gbp. The current step was asking for vegan_count, which is now filled. So the next step would be to request deposit_amount_gbp. But the AI hasn\'t asked that yet. However, the task here is to process the user\'s last message, which is "about 50". The action required is to set the slot and then proceed. Since the user hasn\'t mentioned the deposit yet, the next action would be to start the flow (if not already started) and set the slot. Wait, the active flow is already confirm_booking, so we don\'t need to start it again. The AI\'s next step would be to ask for the deposit amount. But the user hasn\'t provided that yet. So the action here is just to set the vegan_count slot to 50.0. 

Wait, the example in the slot extraction says that when the user says "send money to John", the output includes set slot recipient and start flow. But in this case, the flow is already active. So the correct action is to set the slot. Also, the user\'s message is providing the value for the requested slot. So the action is set slot vegan_count 50.0. 

I need to make sure that the value is in the correct format. The slot\'s type is float, so "50" becomes "50.0".' message='No commands were parsed from the LLM actions.'
2026-04-13 23:54:56 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                          
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                 
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  no thank you                                                                 
Okay, I'll be around in case you need further help.
? How would you rate your experience today? (Use arrow keys)                                
 » 1: 👍 Satisfied (/SetSlots(csat_score=satisfied))
   2: 👎 Not Satisfied (/SetSlots(csat_score=unsatisfied))
   Type out your own message...     
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
2026-04-13 23:57:29 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                     

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                       
And how many of those guests will need vegan meals?

2026-04-13 23:58:44 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user said, "about 50 need vegan." The current flow is confirm_booking, and the current step is asking for vegan_count. The guest_count is already set to 160. So the user is providing the number of vegan guests here.

First, I need to set the vegan_count slot. The user mentioned "about 50," so I should take that as the value. The slot expects a float, so even though it\'s a whole number, I\'ll input it as 50.0. 

Since the user is in the confirm_booking flow and has provided the required slot, the next step would be to ask for the deposit amount. But the user hasn\'t mentioned that yet. The AI should prompt for the next required slot, which is deposit_amount_gbp. However, the task here is to process the user\'s last message, so maybe after setting the slot, the next action is to proceed to the next step in the flow. Wait, the instructions say to output actions based on the user\'s last message. The user provided the vegan_count, so the action is to set that slot. The next step would be the AI asking for the deposit, but that\'s part of the flow\'s next step, not the user\'s message. So the only action here is setting the vegan_count to 50.0. 

I should check if there are any other slots mentioned, but the user only talked about the vegan count. So the action list should be set slot vegan_count 50.0. Also, since the user is in the confirm_booking flow, maybe start flow confirm_booking is needed? Wait, the current active flow is already confirm_booking, so starting it again isn\'t necessary. The example shows that when a user provides info in a flow, you set the slot. So the correct action is just setting the slot. 

Wait, the example for slot extraction says that if the user says "send money to John," you set the recipient and start the transfer_money flow. But in this case, the flow is already active. So maybe no need to start the flow again. The user\'s message is part of the ongoing flow. So the only action is setting the slot. 

But looking at the conversation history, the AI asked for vegan_count, and the user provided it. So the action is to set the slot. Then the system would proceed to the next step in the flow, which is deposit_amount_gbp. But' message='No commands were parsed from the LLM actions.'
2026-04-13 23:58:44 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50                                                         

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £777 deposit                                                     
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £777 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  no bye                                                           
Okay, I'll be around in case you need further help.
? How would you rate your experience today? (Use arrow keys)                    
 » 1: 👍 Satisfied (/SetSlots(csat_score=satisfied))
   2: 👎 Not Satisfied (/SetSlots(csat_score=unsatisfied))
   Type out your own message... 
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £777 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
2026-04-14 00:02:49 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                     

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                       

And how many of those guests will need vegan meals?
Your input ->  can you arrange a parking space for the garlic mobile because we 
will hunt some vampires with holy water and super soakers?                      
2026-04-14 00:06:17 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is asking about arranging a parking space for the "garlic mobile" because they\'re going to hunt vampires with holy water and super soakers. Hmm, first, I need to check the available flows. The current active flow is confirm_booking, which handles booking confirmations with guest count, vegan count, and deposit. But the user\'s request is about parking, which isn\'t part of the confirm_booking flow\'s scope. The handle_out_of_scope flow is meant for things like parking, AV equipment, seating, etc.

So the user\'s main request here is parking arrangement. Since parking isn\'t covered in the confirm_booking flow, I should switch to handle_out_of_scope. But wait, the current flow is confirm_booking. Do I need to cancel it first? The instructions say not to cancel unless the user explicitly requests it. However, if the user is pursuing a different topic, maybe I should start the handle_out_of_scope flow without canceling? Or does starting a new flow automatically cancel the previous one? The examples don\'t show that. Let me check the available actions. The cancel flow action is only to be used when the user explicitly cancels. Since the user hasn\'t canceled the booking confirmation, but is asking about parking, which is out of scope, I should probably start the handle_out_of_scope flow. But the current active flow is confirm_booking. Do I need to cancel it first? The instructions say not to cancel unless the user explicitly requests it. So maybe I can start the handle_out_of_scope flow without canceling the current one. However, the system might be designed to handle only one flow at a time. The user is now asking about parking, which is outside the current flow\'s scope, so maybe the correct action is to start handle_out_of_scope and cancel confirm_booking. Wait, but the user hasn\'t canceled the booking confirmation; they\'re just adding a new request. The general instructions say that multiple flows can be started without canceling if the user pursues several things. But in this case, the user is shifting from booking confirmation to a parking request. Since parking is out of scope for the confirm_booking flow, the handle_out_of_scope flow is the right one. So perhaps the correct action is to start handle_out_of_scope. But the current active flow is confirm_booking. Do I need to cancel it? The instructions say not to cancel unless the user explicitly requests it. The user hasn\'t canceled, so maybe I should start handle_out_of' message='No commands were parsed from the LLM actions.'
2026-04-14 00:06:17 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  garlic mobile                                                    
2026-04-14 00:06:52 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user\'s last message is "garlic mobile". I need to figure out what action to take based on the current state and the conversation history.

First, looking at the current state: the active flow is confirm_booking, and the current step is asking for vegan_count. The user previously provided guest_count as 160, but vegan_count is still undefined. The user\'s latest response is "garlic mobile", which seems unrelated to the number of vegan guests.

The conversation history shows that the user tried to ask about parking for the garlic mobile, but the AI didn\'t understand and repeated the question about vegan meals. Now the user is just saying "garlic mobile" again. Since parking arrangements are outside the scope of the confirm_booking flow (as per the handle_out_of_scope flow description), this request can\'t be addressed in the current flow. 

So, the AI needs to handle this out-of-scope request. The correct action would be to start the handle_out_of_scope flow. However, according to the available actions, starting a flow requires using "start flow flow_name". But wait, the current active flow is confirm_booking, and the user is still in the middle of that. Since the user\'s message is about parking, which is out of scope, but the current flow is confirm_booking, which requires vegan_count, the AI should first acknowledge the out-of-scope request but stay on task.

Wait, the instructions say to use the handle_out_of_scope flow for requests outside booking confirmation. So maybe the correct action is to start handle_out_of_scope. But the user hasn\'t explicitly asked a question about parking again; they just mentioned "garlic mobile" again. The previous attempt was about parking, and now they\'re repeating "garlic mobile". Since parking is out of scope, the AI should respond by indicating it can\'t help with that and get back to the current flow\'s required slot (vegan_count). 

But according to the available actions, the AI can start another flow without canceling the current one. However, the current flow is confirm_booking, which is still active. The user\'s message is unrelated to the current slot being asked (vegan_count), so the AI should handle the out-of-scope part but also prompt again for the required slot. 

Wait, the task is to create an action list based on the user\'s last message. The user\'s message is "garlic mobile". The AI needs to process this. Since parking is' message='No commands were parsed from the LLM actions.'
2026-04-14 00:06:52 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  what about ninja turtles? do they like pizza?                    
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes                                                              
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200                                                             
2026-04-14 00:07:52 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is in the middle of confirming a booking. The current flow is confirm_booking, and the active step is asking for the deposit amount in GBP. The user just replied with "£200". 

First, I need to set the deposit_amount_gbp slot to 200. Since the user provided the amount, I should convert that into the set slot action. The value should be a float, so 200.0 maybe? But the user wrote £200, so the numerical part is 200. The slot expects a float, so "200.0" would be correct.

Now, check if there are any other slots that need to be filled. The guest_count is already set to 160.0, and vegan_count is still undefined. But the user hasn\'t mentioned anything about vegan meals yet. The previous attempts were about parking and ninja turtles, which were out of scope. So the next step after deposit is probably to check if all required slots are filled. Wait, the confirm_booking flow\'s slots are guest_count, vegan_count, and deposit_amount_gbp. The required slots might be all three. But the user hasn\'t provided vegan_count yet. However, the user\'s last message was about the deposit, so maybe after setting deposit_amount_gbp, the system should prompt again for vegan_count if it\'s still missing. But according to the current state, the requested_slot was deposit_amount_gbp. Once that\'s filled, maybe the flow is complete? Or is there another step? Let me check the flow description again. The confirm_booking flow is triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements (vegan_count), and deposit terms. So all three slots are needed. But in the current state, vegan_count is still undefined. However, the user hasn\'t been asked again yet. The AI had asked about vegan meals before, but the user went off-topic. Now, after the deposit is provided, maybe the next step is to check if vegan_count is still missing and prompt again. But the user\'s last message was just the deposit. So the action here is to set the deposit slot and then proceed. Since the user answered the deposit, the flow might proceed to the next step, which is to confirm all details. But the current step was specifically asking for deposit_amount_gbp. Once that\'s filled, maybe the flow is done, and the system' message='No commands were parsed from the LLM actions.'
2026-04-14 00:07:52 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                     

2026-04-14 00:08:17 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is in the middle of confirming a booking. The current flow is confirm_booking, and the active step is asking for the deposit amount in GBP. The user has already provided the guest count as 160, but the vegan count is still undefined. The deposit amount was asked twice, and the user finally said "£200 deposit".

First, I need to extract the deposit amount. The user mentioned £200, so I should set the deposit_amount_gbp slot to 200. The current step is specifically asking for this, so that\'s straightforward. The action would be "set slot deposit_amount_gbp 200.0" since the slot expects a float.

Next, check if there are any other slots mentioned. The user didn\'t mention anything about vegan meals here, so the vegan_count remains undefined. Since the last message is about the deposit, there\'s no need to set another slot. 

Now, considering the flow. The confirm_booking flow is active, and after setting the deposit, the next step would typically be to confirm all details or proceed with the booking. However, the instructions say to take it one step at a time. Since the user provided the deposit amount, the AI should acknowledge and maybe move to the next required slot, which is vegan_count. But the user hasn\'t mentioned that yet. Wait, looking at the conversation history, the AI previously asked about vegan meals, and the user went off on tangents about garlic mobile and ninja turtles. The AI redirected back to the booking. Now, after the deposit is set, the next step should be to ask for the vegan count again. But the task is to respond to the user\'s last message, which is the deposit. So the immediate action is to set the deposit slot. The next step (asking about vegan meals) would be part of the flow\'s next step, but since the user hasn\'t provided that info yet, maybe the AI should prompt again. However, the task here is only to process the last message. So the only action needed is setting the deposit_amount_gbp. 

Also, check if there\'s any out-of-scope request here. The user\'s message is "£200 deposit", which is directly related to the deposit amount. No off-topic or out-of-scope elements here. So no need to trigger handle_out_of_scope. 

So the action list should be just setting the deposit slot. The start flow is already' message='No commands were parsed from the LLM actions.'
2026-04-14 00:08:17 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                     

Thank you — booking confirmed. 160 guests, 0 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  no                                                               
Okay, I'll be around in case you need further help.
? How would you rate your experience today? (Use arrow keys)                    
 » 1: 👍 Satisfied (/SetSlots(csat_score=satisfied))
   2: 👎 Not Satisfied (/SetSlots(csat_score=unsatisfied))
   Type out your own message..
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
The agent was able to handle the out of scope request gracefully, mentioning that it can only help with confirming tonight's venue booking.
However, it skipped the vegan count slot and went straight to the deposit amount slot.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """ The agent was polite but it didn't give a clear response to the out of scope request, like the second question. IT might
be my fault as I tried something that doesn't make much sense. The agent however, tried to get me on the topic of the booking which was good. One thing,
it skipped the vegan count slot and went straight to the deposit amount slot.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = None   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"] #line 118 to 123

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
FILL ME IN
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
We are using Rasa Pro CALM which is a more advanced version of Rasa. It uses a language model to understand the user's intent and then uses a flow to execute the action. The language model is able to understand the user's intent and then use the flow to execute the action. The flow is able to execute the action based on the user's intent.
Think about:
- What does the LLM handle now that Python handled before? - the language model is able to understand the user's intent and then use the flow to execute the action. The flow is able to execute the action based on the user's intent.
- What does Python STILL handle, and why (hint: business rules)? - tools, business rules like venue capacity and deposit amount.
- Is there anything you trusted more in the old approach? - the old approach was more reliable and predictable. 
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
FILL ME IN

Be specific. What can the Rasa CALM agent NOT do that LangGraph could?
Is that a feature or a limitation for the confirmation use case?
Think about: can the CALM agent improvise a response it wasn't trained on?
Can it call a tool that wasn't defined in flows.yml?
"""
