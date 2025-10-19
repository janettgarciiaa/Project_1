# --- Claude Response Section ---
if context_from_search:
    claude_messages.append({
        "role": "user",
        "content": f"{prompt}\n\n{context_from_search}"
    })
else:
    claude_messages.append({
        "role": "user",
        "content": prompt
    })

assistant_text = None
error_text = None

try:
    # Combine user input and context into one message for the REST call
    full_prompt = f"{system_prompt}\n\n" + "\n".join(
        msg["content"] for msg in claude_messages if msg["role"] == "user"
    )

    # Call Claude via REST API (avoids SDK issues on Streamlit Cloud)
    assistant_text = ask_claude_via_rest(full_prompt)

# --- Claude Response Section ---
if context_from_search:
    claude_messages.append({
        "role": "user",
        "content": f"{prompt}\n\n{context_from_search}"
    })
else:
    claude_messages.append({
        "role": "user",
        "content": prompt
    })

assistant_text = None
error_text = None

try:
    # Combine user input and context into one message for the REST call
    full_prompt = f"{system_prompt}\n\n" + "\n".join(
        msg["content"] for msg in claude_messages if msg["role"] == "user"
    )

    # Call Claude via REST API (avoids SDK issues on Streamlit Cloud)
    assistant_text = ask_claude_via_rest(full_prompt)

except Exception as e:
    error_text = str(e)

# --- Display Assistant Response ---
with st.chat_message("assistant"):
    if assistant_text:
        if sources_md:
            st.markdown(sources_md)
            st.markdown("---")
        st.markdown(assistant_text)
    else:
        if sources_md:
            st.markdown(sources_md)
            st.info("Showing sources only — Claude response unavailable.")
        else:
            st.error("Could not generate a response. " + (error_text or ""))
        if search_note:
            st.caption(search_note)

# --- Save Assistant Message to Chat State ---
st.session_state.messages.append({
    "role": "assistant",
    "content": assistant_text if assistant_text else (sources_md or "(no response)")
})

