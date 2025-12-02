import streamlit as st
import google.generativeai as genai

# ==========================================
# PART 1: EXPANDED LOCAL TEMPLATE LIBRARY
# ==========================================

# We structure this by Language -> Keyword -> Code
LOCAL_TEMPLATES = {
    "Python": {
        "hello": "print('Hello, World!')",
        "factorial": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)",
        "fibonacci": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a, end=' ')\n        a, b = b, a + b",
        "prime": "def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0: return False\n    return True",
        "bubble sort": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
        "palindrome": "def is_palindrome(s):\n    return s == s[::-1]",
        "calculator": "def add(x, y): return x + y\ndef subtract(x, y): return x - y\ndef multiply(x, y): return x * y\ndef divide(x, y): return x / y if y != 0 else 'Error'",
        "reverse string": "def reverse_string(s):\n    return s[::-1]",
        "even odd": "def check_even_odd(n):\n    return 'Even' if n % 2 == 0 else 'Odd'",
        "sum array": "def sum_array(arr):\n    return sum(arr)",
        "binary search": "def binary_search(arr, x):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (high + low) // 2\n        if arr[mid] < x: low = mid + 1\n        elif arr[mid] > x: high = mid - 1\n        else: return mid\n    return -1"
    },
    "Java": {
        "hello": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
        "factorial": "public class Factorial {\n    public static int factorial(int n) {\n        if (n == 0) return 1;\n        return n * factorial(n - 1);\n    }\n}",
        "fibonacci": "public class Fibonacci {\n    public static void main(String[] args) {\n        int n = 10, t1 = 0, t2 = 1;\n        for (int i = 1; i <= n; ++i) {\n            System.out.print(t1 + \" \");\n            int sum = t1 + t2;\n            t1 = t2;\n            t2 = sum;\n        }\n    }\n}",
        "prime": "public class Prime {\n    public static boolean isPrime(int n) {\n        if (n <= 1) return false;\n        for (int i = 2; i <= Math.sqrt(n); i++) {\n            if (n % i == 0) return false;\n        }\n        return true;\n    }\n}",
        "bubble sort": "import java.util.Arrays;\npublic class BubbleSort {\n    static void bubbleSort(int array[]) {\n        int size = array.length;\n        for (int i = 0; i < size - 1; i++)\n            for (int j = 0; j < size - i - 1; j++)\n                if (array[j] > array[j + 1]) {\n                    int temp = array[j];\n                    array[j] = array[j + 1];\n                    array[j + 1] = temp;\n                }\n    }\n}"
    },
    "JavaScript": {
        "hello": "console.log('Hello, World!');",
        "factorial": "function factorial(n) {\n  if (n === 0) return 1;\n  return n * factorial(n - 1);\n}",
        "fibonacci": "function fibonacci(n) {\n  let a = 0, b = 1, temp;\n  for (let i = 0; i < n; i++) {\n    console.log(a);\n    temp = a + b;\n    a = b;\n    b = temp;\n  }\n}",
        "palindrome": "function isPalindrome(str) {\n  const reversed = str.split('').reverse().join('');\n  return str === reversed;\n}"
    },
    "C++": {
        "hello": "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello, World!\";\n    return 0;\n}",
        "factorial": "#include <iostream>\nusing namespace std;\nint factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n - 1);\n}",
        "fibonacci": "#include <iostream>\nusing namespace std;\nint main() {\n    int n = 10, t1 = 0, t2 = 1, nextTerm = 0;\n    for (int i = 1; i <= n; ++i) {\n        if(i == 1) {\n            cout << t1 << \", \";\n            continue;\n        }\n        if(i == 2) {\n            cout << t2 << \", \";\n            continue;\n        }\n        nextTerm = t1 + t2;\n        t1 = t2;\n        t2 = nextTerm;\n        cout << nextTerm << \", \";\n    }\n    return 0;\n}"
    },
    # Fallback for C if selected
    "C": {
        "hello": "#include <stdio.h>\nint main() {\n   printf(\"Hello, World!\");\n   return 0;\n}"
    }
}

# ==========================================
# PART 2: AI LOGIC (The Brain)
# ==========================================

# --- CONFIGURATION ---
api_key = "AIzaSyC7IxZTXdXC6BgVHHd6eGUvc1riE54lhLU"  # <--- PASTE YOUR API KEY HERE

if api_key == "YOUR_GEMINI_API_KEY":
    st.error("⚠️ Please put your actual Gemini API Key in the code.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_response(prompt_text):
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"

def generate_code_logic(user_prompt, language="Python"):
    # 1. CLEAN THE PROMPT
    prompt_lower = user_prompt.lower()
    
    # 2. CHECK LOCAL TEMPLATES FOR THE SELECTED LANGUAGE
    # We only look inside the dictionary of the selected language
    if language in LOCAL_TEMPLATES:
        for key, code in LOCAL_TEMPLATES[language].items():
            if key in prompt_lower:
                return f"// [LOCAL TEMPLATE: {language} - {key.upper()}]\n{code}"
            
    # 3. IF NOT FOUND, USE GEMINI API
    prompt = f"You are an expert coder. Write a clean, efficient code snippet in {language} for the following task: {user_prompt}. Only provide the code, no markdown formatting."
    return get_gemini_response(prompt)

def analyze_code_logic(code_snippet):
    prompt = f"Analyze the following code. Explain: 1. Logic Flow. 2. Time/Space Complexity. 3. Potential errors. Code: {code_snippet}"
    return get_gemini_response(prompt)

def document_code_logic(code_snippet):
    prompt = f"Take the following code and add detailed docstrings and inline comments. Return the full code. Code: {code_snippet}"
    return get_gemini_response(prompt)

def get_algorithm_logic(code_snippet):
    prompt = f"Read the following code and extract the Step-by-Step Algorithm in plain English (Step 1, Step 2...). Code: {code_snippet}"
    return get_gemini_response(prompt)

# ==========================================
# PART 3: APP UI (The Frontend)
# ==========================================

st.set_page_config(page_title="AutoCoder", layout="wide")

st.title("🤖 AutoCoder: Universal Code Intelligence")
st.markdown("Generate, Analyze, Document, and Extract Algorithms using AI.")

# --- SIDEBAR ---
st.sidebar.title("Configuration")
language = st.sidebar.selectbox("Select Target Language", ["Python", "Java", "C++", "JavaScript", "C"])

# --- MAIN TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Code Generator", 
    "🔍 Code Analyzer", 
    "📄 Auto-Documentation", 
    "🧠 Algorithm Extractor"
])

# === TAB 1: CODE GENERATOR ===
with tab1:
    st.header(f"Generate {language} Code")
    user_prompt = st.text_area("Describe the code you need:", height=150, placeholder=f"Example: 'factorial' or 'bubble sort'")
    
    if st.button("Generate Code", key="btn_gen"):
        if user_prompt:
            # Check for local template match to show correct status
            is_local = False
            if language in LOCAL_TEMPLATES:
                for key in LOCAL_TEMPLATES[language]:
                    if key in user_prompt.lower():
                        is_local = True
                        break
            
            if is_local:
                st.success(f"⚡ Instant Result! (Local {language} Template)")
                result = generate_code_logic(user_prompt, language)
                st.code(result, language=language.lower())
            else:
                with st.spinner(f"🤖 Generating {language} code via AI..."):
                    result = generate_code_logic(user_prompt, language)
                    st.code(result, language=language.lower())
        else:
            st.warning("Please enter a description.")

# === TAB 2: CODE ANALYZER ===
with tab2:
    st.header("Analyze Code Logic & Complexity")
    code_input_analyze = st.text_area("Paste your code here for analysis:", height=200)
    
    if st.button("Analyze Code", key="btn_analyze"):
        if code_input_analyze:
            with st.spinner("Analyzing..."):
                result = analyze_code_logic(code_input_analyze)
                st.markdown(result)

# === TAB 3: AUTO-DOCUMENTATION ===
with tab3:
    st.header("Add Docstrings & Comments")
    code_input_doc = st.text_area("Paste code to document:", height=200)
    
    if st.button("Generate Documentation", key="btn_doc"):
        if code_input_doc:
            with st.spinner("Documenting..."):
                result = document_code_logic(code_input_doc)
                st.code(result, language=language.lower())

# === TAB 4: ALGORITHM EXTRACTOR ===
with tab4:
    st.header("Extract Algorithm")
    code_input_algo = st.text_area("Paste code to extract algorithm:", height=200)
    
    if st.button("Get Algorithm", key="btn_algo"):
        if code_input_algo:
            with st.spinner("Extracting..."):
                result = get_algorithm_logic(code_input_algo)
                st.markdown(result)

st.markdown("---")
st.caption("Built with Python, Streamlit & Gemini API")