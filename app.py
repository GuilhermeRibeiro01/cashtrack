import streamlit as st
import requests 

ENDPOINT_URL = "https://fm5l1lifv8.execute-api.sa-east-1.amazonaws.com/execute"

st.title("💬 Chatbot")

# try:
#     response = requests.get(ENDPOINT_URL + "/company")
#     if response.status_code == 200:
#         companies = response.json()
#         print('companies', companies)
#         company_id_options = [company["name"] for company in companies]
#     else:
#         st.error("Falha ao obter a lista de empresas. Por favor, tente novamente.")
#         st.stop()
# except Exception as e:
#     st.error(f"Um erro ocorreu: {str(e)}")
#     st.stop()

# selected_company_name = st.selectbox("Empresa", company_id_options)

# selected_company_id = next(
#     (company['id'] for company in companies if company["name"] == selected_company_name),
#     None,
# )

# product_id = st.selectbox("Tipo de seguro", ["Vida", "Automóvel"])

# print('selected_company_id', selected_company_id)

models = {
    "claude-v3-5-sonnet":"anthropic.claude-3-5-sonnet-20240620-v1:0",
    "claude-v3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
}

model_id_options = list(models.keys())

selected_model_id = st.selectbox("Modelo", model_id_options)

# chosen_company_id = selected_company_id
chosen_model_id = models[selected_model_id]

user_id = st.text_input("ID do usuário")
empresa_id = st.text_input("ID da empresa")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Como posso ajudar você?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    request_data = {
        "question": prompt,
        "modelId": chosen_model_id,
        "userId": user_id,
        "empresaId": empresa_id
    }

    print('request_data', request_data)

    try:
        response = requests.post(ENDPOINT_URL, json=request_data)
        print("RESPONSE::: ", response)
        if response.status_code == 200:
            response_data = response.json()
            print("RESPONSE: ", response_data)
            response_text = response_data["output"]

            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
            st.chat_message("assistant").write(response_text)

            print(f"Response data: {response_data}")
        else:
            st.error("Falhou em obter uma resposta da api.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar enviar o pedido.")