import streamlit as st #Aviso del uso de la libreria
from groq import Groq #Importamos la libreria

#Configuración de la ventana de la web
st.set_page_config(page_title="Mi chat de IA", page_icon="🤖")
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
#Nos conecta con la API, creando un usuario
def crear_usuario_groq():
    #Obtenemos la clave de la API
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta) #Conectamos a la API

#Selecciona el modelo de la IA
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #Seleccion el modelo de IA
        messages = [{"role":"user", "content" : mensajeDeEntrada}],
        stream = True #Funcionalidad para IA, responde a tiempo real
    ) #Devuelve la respuesta que manda la IA

#Historial de mensaje
def inicilizar_estado():
    #si no exite "mensajes" entonces creamos un historial
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Historial vacio

def configurar_pagina():
    st.title("Mi chat de IA") #Titulo
    st.sidebar.title("Configuración") #Titulo
    opcion = st.sidebar.selectbox(
        "Elegí modelo", #titulo
        options = MODELOS, #opiciones deben estar en una lista
        index = 0 #valorPorDefecto
    )
    return opcion #! AGREAMOS ESTO PARA OBTENER EL NOMBRE DEL MODELO

def actualizar_historial(rol, contenido, avatar): 
    #El metodo append(dato) Agrega datos a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial(): #Guarda la estructura visual del mensaje
    for mensaje in st.session_state.mensajes: 
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) :
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    with contenedorDelChat : mostrar_historial()

#! NUEVA FUNCIÓN
def generar_respuesta(chat_completo):
    respuesta_completa = "" #variable vacia
    for frase in chat_completo:
        if frase.choices[0].delta.content: #Evitamos el dato NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    
    return respuesta_completa

def main():
    #? INVOCACIÓN DE FUNCIONES
    modelo = configurar_pagina() #Agarramos el modelo seleccionado
    clienteUsuario = crear_usuario_groq() #Conecta con la API GROQ
    inicilizar_estado() #Se crea en memoria el historial vacio
    area_chat() #Se crea el contenedor de los mensajes
    mensaje = st.chat_input("Escribí un mensaje...")
    #! MODIFICAMOS EL CODIGO DEL IF
    if mensaje:
        actualizar_historial("user", mensaje, "🤷‍♀️") #Mostramos el mensaje en el chat
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #Obtenemos la respuesta de IA
        if chat_completo: #verficamos que la variable tenga algo
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun() #Actualizar

if __name__ == "__main__": 
    main() 