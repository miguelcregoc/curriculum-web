import json
import os
import boto3

sns = boto3.client("sns")                  # fuera del handler: se reutiliza
TOPIC_ARN = os.environ["TOPIC_ARN"]        # variable de entorno que le pase a lambda

MAX_ASUNTO = 99
MAX_EMAIL = 150
MAX_MENSAJE = 1000


def respuesta(codigo, texto):
    # Devuelve el diccionario que espera API Gateway
    return {
        "statusCode": codigo,
        "body": json.dumps({"mensaje": texto}),
    }


def lambda_handler(event, context):
    # leo el body (texto) y convertirlo a diccionario.
    # Si no existe o el JSON está roto -> 400
    try:
        datos = json.loads(event.get("body"))
    except (TypeError, json.JSONDecodeError):
        return respuesta(400, "texto vacio o json no valido")

    if not (isinstance(asunto, str) and isinstance(email, str) and isinstance(mensaje, str)):
            return respuesta(400, "los campos deben ser texto")


    # Saco los campos
    asunto = datos.get("asunto", "")
    email = datos.get("email", "")
    mensaje = datos.get("mensaje", "")

    # compruebo que son texto
    if not (isinstance(asunto, str) and isinstance(email, str) and isinstance(mensaje, str)):
        return respuesta(400, "los campos deben ser texto")

    # quito espacios sobrantes
    asunto = asunto.strip()
    email = email.strip()
    mensaje = mensaje.strip()
    

    # valido que los campos no esten vacios ni sobrepasen la longitud max
    if not asunto or len(asunto) > MAX_ASUNTO:
        return respuesta(400, "asunto no valido")
    if not email or len(email) > MAX_EMAIL:
        return respuesta(400, "email no valido")
    if not mensaje or len(mensaje) > MAX_MENSAJE:
        return respuesta(400, "mensaje no valido")

    # cambio los saltos de linea por espacio
    asuntoLimpio = asunto.replace("\n", " ") 
    cuerpo = "Correo de " + email + "\n" + mensaje

    
    try:
        sns.publish(TopicArn=TOPIC_ARN, Subject=asuntoLimpio, Message=cuerpo)
    except Exception:
        return respuesta(500, "no se pudo enviar el mensaje") #si falla

    return respuesta(200, "mensaje enviado")