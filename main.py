# --- Claude Chatbot Response Section ---

try:
    # Prepare user prompt with optional context from web search
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

    # Combine all user prompts into one string for Claude REST call
    full_prompt = f"{system_prompt}\n\n" + "\n".join(
        msg["content"] for msg in claude_messages if msg["role"] == "user"
    )

    # Call Claude using REST API (this avoids Anthropic SDK proxy errors)
    assistant_text = ask_claude_via_rest(full_prompt)

except Exception as e:
    # If anything goes wrong, capture the error
    error_text = str(e)
    assistant_text = None

# --- Display the Assistant’s Response in Streamlit ---
with st.chat_message("assistant"):
    if assistant_text:
        # Display any web search sources first
        if sources_md:
            st.markdown(sources_md)
            st.markdown("---")
        # Then display Claude’s message
        st.markdown(assistant_text)
    else:
        # If no Claude response, show an error or sources
        if sources_md:
            st.markdown(sources_md)
            st.info("Showing sources only — Claude response unavailable.")
        else:
            st.error("Could not generate a response. " + (error_text or ""))
        if search_note:
            st.caption(search_note)

# --- Save the Assistant’s Message to Chat State ---
st.session_state.messages.append({
    "role": "assistant",
    "content": assistant_text if assistant_text else (sources_md or "(no response)")
})

