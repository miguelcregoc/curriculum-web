import json
import os
import boto3

sns = boto3.client("sns")          # fuera del handler: se reutiliza
TOPIC_ARN = os.environ[...]        # ¿qué clave guardaste en la variable de entorno?

MAX_NOMBRE = 100
MAX_EMAIL = 150
MAX_MENSAJE = 1000


def respuesta(codigo, texto):
    # Devuelve el diccionario que espera API Gateway
    return {
        "statusCode": ...,
        "body": json.dumps({"mensaje": ...}),
    }


def lambda_handler(event, context):
    # 1. Leer el body (texto) y convertirlo a diccionario.
    #    Si no existe o el JSON está roto -> 400
    try:
        datos = json.loads(...)
    except (...):
        return respuesta(400, "...")

    # 2. Sacar los tres campos y quitar espacios sobrantes
    nombre = datos.get("nombre", "")...
    email = ...
    mensaje = ...

    # 3. Validar: no vacíos y dentro de la longitud máxima -> si no, 400
    ...

    # 4. Construir Subject (máx. 100 caracteres, sin saltos de línea) y Message
    asunto = ...
    cuerpo = ...

    # 5. Publicar en SNS. Si falla -> 500 (sin revelar detalles internos)
    try:
        sns.publish(TopicArn=..., Subject=..., Message=...)
    except Exception:
        return respuesta(500, "...")

    return respuesta(200, "...")