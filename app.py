import gradio as gr

from answer import answer_question

def format_context(context):
    result = "<h2 style='color: #ff7800;'>Relevant Context</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result

# sends latest question and previous messages to answer_question
# then appends the assistant's response and returns the updated chat plus retrieved context
def chat(history):
    last_message = history[-1]["content"]
    prior = history[:-1]
    answer, context = answer_question(last_message, prior)
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)

def main():
    # add the user message to chat
    # clears the textbox
    def put_message_in_chatbot(message, history):
        return "", history + [{"role": "user", "content": message}]

    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title="My Personal Assistant", theme=theme) as ui:
        gr.Markdown("# My Personal Assistant\nAsk me anything about yourself!")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="Conversation", height=600, type="messages", show_copy_button=True
                )
                message = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about yourself...",
                    show_label=False
                )

            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    label="Retrieved Context",
                    value="*Retrieved context will appear here*",
                    height=600
                )

        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

    ui.launch(
        share=True,
        server_port=7861
        )

if __name__ == "__main__":
    main()