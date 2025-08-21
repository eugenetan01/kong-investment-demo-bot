
import os

import json
import requests
import streamlit as st


# --- Settings (override via env vars) ---
ENDPOINT_URL = st.secrets["ENDPOINT_URL"]
MESSAGES_TEMPLATE = st.secrets["MESSAGES_TEMPLATE"]
APIKEY = st.secrets["API_KEY"]

# --- Load quiz spec ---
with open("questions.json", "r", encoding="utf-8") as f:
    QUIZ = json.load(f)

st.set_page_config(page_title="Kong Investment Quiz", page_icon="🦍", layout="centered")

# Header
cols = st.columns([1,5])
with cols[0]:
    st.image("assets/kong-logo.png", use_column_width=True)
with cols[1]:
    st.markdown("# Investment Profile Quiz")
    st.caption("Personal Financial Advisor • Powered by Kong")

st.divider()

with st.form("quiz_form"):
    name = st.text_input("Name", placeholder="Enter your name", help="Will be sent as the 'user' property.")
    st.write("### Questionnaire")
    selections = {}

    for q in QUIZ["questions"]:
        key = q["id"]
        labels = [opt["label"] for opt in q["options"]]
        default_idx = 0
        choice = st.radio(f"**{q['title']}**\n{q['question']}", labels, index=default_idx, key=key)
        # Map back to value & points
        chosen = next(o for o in q["options"] if o["label"] == choice)
        selections[key] = {"value": chosen["value"], "label": chosen["label"]}


    submitted = st.form_submit_button("Submit", use_container_width=True)
    st.caption("By submitting, your selections will be sent to the configured endpoint via POST.")

if submitted:
    if not name.strip():
        st.error("Please enter your name.")
    else:
        # Build payload
        properties = {
            "user": name.strip(),
            "timeline": selections["timeline"]["value"],
            "risk": selections["risk"]["value"],
            "volatility": selections["volatility"]["value"],
            "experience": selections["experience"]["value"],
            "ultimate_goal": selections["ultimate_goal"]["value"],
        }
        payload = {
            "messages": MESSAGES_TEMPLATE,
            "properties": properties,
        }

        # Headers
        headers = {
            "Content-Type": "application/json",
            "apikey": APIKEY
        }


        # Preview curl
        curl_props = json.dumps(payload, ensure_ascii=False)
        curl_preview = f"""curl --request POST \\n  --url {ENDPOINT_URL} \\n  --header 'Content-Type: application/json' --data '{{curl_props}}'"""
        with st.expander("Preview request (cURL)"):
            st.code(curl_preview, language="bash")
        resp = None

        # Send request
        try:
            with st.spinner("Fetching your investment advice..."):
                resp = requests.post(ENDPOINT_URL, headers=headers, json=payload, timeout=30)

            display = st.success if resp.ok else st.error
            display(f"Request sent. Status: {resp.status_code}")

            # Try to show JSON if available
            try:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                #st.write(content)
                if content:
                    # how to make carriage return after advice?
                    st.success(f"Investment Advice: \n\n{content}")
                else:
                    st.write(content)
            except Exception:
                st.error("Sorry, there appears to be illegal or prohibited activities in your input. I can’t advise on that. Please consider legal investment choices.")
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")

        # with st.expander("Your selections"):
        #    st.write({k: v for k, v in selections.items()})
