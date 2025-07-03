import google.generativeai as genai
API_KEY_GEMINI = 'AIzaSyCfLxMy7C0GB61RMiC3EGtwtNJxVL6-zVA' # Remember to use environment variables for real projects!
question = 'compare the performance of IBM with microsoft for the last quarter'

genai.configure(api_key=API_KEY_GEMINI)
model = genai.GenerativeModel("gemini-1.5-flash")
# It's good practice to add error handling for cases where no models are found
# try:
#     models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
#     if not models:
#         print("No models supporting 'generateContent' found. Please check your API key and network connection.")
#         exit() # Exit if no suitable model is found

#     # Select the first available model that supports content generation
#     # For better control, you might want to explicitly choose a model like 'gemini-pro' or 'gemini-1.5-flash'
#     model_name_to_use = models[0].name
#     model = genai.GenerativeModel(model_name_to_use)
#     print(f"Using Model : {model}") # Print the actual model name being used

# except Exception as e:
#     print(f"Error during model discovery or selection: {e}")
#     exit()

# The crucial change is here: call generate_content on the 'model' object
try:
    completion = model.generate_content(
        contents=question,
        
    )

    # Check for content filtering or other issues before accessing .result
    if completion.prompt_feedback and completion.prompt_feedback.block_reason:
        print(f"Prompt was blocked due to: {completion.prompt_feedback.block_reason}")
    elif not completion.candidates:
        print("No content candidates were generated for the prompt.")
    else:
        gemini_res = completion.text # .text is a convenient way to get the content of the first candidate
        print("\n--- Gemini's Response ---")
        print(gemini_res)

except Exception as e:
    print(f"An error occurred during content generation: {e}")
    # Consider importing 'traceback' and using 'traceback.print_exc()' for full error details in debugging